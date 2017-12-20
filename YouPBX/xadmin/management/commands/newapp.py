# coding=utf-8

import os
import shutil

from django.core.management.base import CommandError, BaseCommand
from django.utils.importlib import import_module


class Command(BaseCommand):
    help = (u"Creates a new Django app.")

    def handle(self, app_name=None, *args, **options):
        if app_name is None:
            raise CommandError(u"you must provide an app name")

        # Check that the app_name cannot be imported.
        try:
            import_module(app_name)
        except ImportError:
            pass
        else:
            raise CommandError(u"The app with the name of %r already exists" % app_name)

        cur = os.path.dirname(__file__)
        par = os.path.dirname(cur)
        shutil.copytree( os.path.join(par,'app_template'), './%s'%app_name)
