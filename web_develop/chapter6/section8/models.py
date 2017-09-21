# coding=utf-8
import os
import uuid
import magic
import urllib
from datetime import datetime

import cropresize2
import short_url
from PIL import Image
from flask import abort, request
from werkzeug.utils import cached_property
from mongoengine import (
    Document as BaseDocument, connect, ValidationError, DoesNotExist,
    QuerySet, MultipleObjectsReturned, IntField, DateTimeField, StringField,
    SequenceField)

from mimes import IMAGE_MIMES, AUDIO_MIMES, VIDEO_MIMES
from utils import get_file_md5, get_file_path

connect('r', host='localhost', port=27017)


class BaseQuerySet(QuerySet):
    def get_or_404(self, *args, **kwargs):
        try:
            return self.get(*args, **kwargs)
        except (MultipleObjectsReturned, DoesNotExist, ValidationError):
            abort(404)


class Document(BaseDocument):
    meta = {'abstract': True,
            'queryset_class': BaseQuerySet}


class PasteFile(Document):
    id = SequenceField(primary_key=True)
    filename = StringField(max_length=5000, null=False)
    filehash = StringField(max_length=128, null=False, unique=True)
    filemd5 = StringField(max_length=128, null=False, unique=True)
    uploadtime = DateTimeField(null=False)
    mimetype = StringField(max_length=128, null=False)
    size = IntField(null=False)
    meta = {'collection': 'paste_file'}  # 自定义集合的名字

    def __init__(self, filename='', mimetype='application/octet-stream',
                 size=0, filehash=None, filemd5=None, *args, **kwargs):
        # 初始化父类的__init__方法
        super(PasteFile, self).__init__(filename=filename, mimetype=mimetype,
                                        size=size, filehash=filehash,
                                        filemd5=filemd5, *args, **kwargs)
        self.uploadtime = datetime.now()
        self.mimetype = mimetype
        self.size = int(size)
        self.filehash = filehash if filehash else self._hash_filename(filename)
        self.filename = filename if filename else self.filehash
        self.filemd5 = filemd5

    @staticmethod
    def _hash_filename(filename):
        _, _, suffix = filename.rpartition('.')
        return '%s.%s' % (uuid.uuid4().hex, suffix)

    @cached_property
    def symlink(self):
        return short_url.encode_url(self.id)

    @classmethod
    def get_by_symlink(cls, symlink, code=404):
        id = short_url.decode_url(symlink)
        return cls.objects.get_or_404(id=id)

    @classmethod
    def get_by_filehash(cls, filehash, code=404):
        return cls.objects.get_or_404(filehash=filehash)

    @classmethod
    def get_by_md5(cls, filemd5):
        rs = cls.objects(filemd5=filemd5)
        return rs[0] if rs else None

    @classmethod
    def create_by_upload_file(cls, uploaded_file):
        rst = cls(uploaded_file.filename, uploaded_file.mimetype, 0)
        uploaded_file.save(rst.path)
        with open(rst.path) as f:
            filemd5 = get_file_md5(f)
            uploaded_file = cls.get_by_md5(filemd5)
            if uploaded_file:
                os.remove(rst.path)
                return uploaded_file
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        rst.filemd5 = filemd5
        return rst

    @classmethod
    def create_by_old_paste(cls, filehash):
        filepath = get_file_path(filehash)
        mimetype = magic.from_file(filepath, mime=True)
        filestat = os.stat(filepath)
        size = filestat.st_size

        rst = cls(filehash, mimetype, size, filehash=filehash)
        return rst

    @property
    def path(self):
        return get_file_path(self.filehash)

    def get_url(self, subtype, is_symlink=False):
        hash_or_link = self.symlink if is_symlink else self.filehash
        return 'http://{host}/{subtype}/{hash_or_link}'.format(
            subtype=subtype, host=request.host, hash_or_link=hash_or_link)

    @property
    def url_i(self):
        return self.get_url('i')

    @property
    def url_p(self):
        return self.get_url('p')

    @property
    def url_s(self):
        return self.get_url('s', is_symlink=True)

    @property
    def url_d(self):
        return self.get_url('d')

    @property
    def image_size(self):
        if self.is_image:
            im = Image.open(self.path)
            return im.size
        return (0, 0)

    @property
    def quoteurl(self):
        return urllib.quote(self.url_i)

    @classmethod
    def rsize(cls, old_paste, weight, height):
        assert old_paste.is_image, TypeError('Unsupported Image Type.')

        img = cropresize2.crop_resize(
            Image.open(old_paste.path), (int(weight), int(height)))

        rst = cls(old_paste.filename, old_paste.mimetype, 0)
        img.save(rst.path)
        filestat = os.stat(rst.path)
        rst.size = filestat.st_size
        return rst

    @property
    def is_image(self):
        return self.mimetype in IMAGE_MIMES

    @property
    def is_audio(self):
        return self.mimetype in AUDIO_MIMES

    @property
    def is_video(self):
        return self.mimetype in VIDEO_MIMES

    @property
    def is_pdf(self):
        return self.mimetype == 'application/pdf'

    @property
    def type(self):
        for t in ('image', 'pdf', 'video', 'audio'):
            if getattr(self, 'is_' + t):
                return t
        return 'binary'
