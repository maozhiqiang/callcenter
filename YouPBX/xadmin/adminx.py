# coding=utf-8
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType

import xadmin
from models import UserSettings


class UserSettingsAdmin(object):
    model_icon = 'fa fa-cog'
    hidden_menu = False
xadmin.site.register(UserSettings, UserSettingsAdmin)


class LogEntryAdmin(object):
    list_display = ['id', '__str__', 'object_id', 'content_type', 'user', 'action_time']
    list_filter = ['content_type']
    app_label = 'xadmin'
xadmin.site.register(LogEntry, LogEntryAdmin)

class ContentTypeAdmin(object):
    app_label = 'xadmin'
xadmin.site.register(ContentType, ContentTypeAdmin)