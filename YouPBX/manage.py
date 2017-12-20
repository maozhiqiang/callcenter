#!/usr/bin/env python
import os
import sys

import gevent.monkey
gevent.monkey.patch_all()

if __name__ == "__main__":
    PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
    sys.path.insert(0, os.path.join(PROJECT_ROOT, 'lib'))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
