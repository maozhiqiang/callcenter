# coding=utf-8

from xadmin import site
from xadmin.views.dashboard import AppDashboard

site.site_title = 'YouPBX'
site.site_footer  = 'Oejia CopyRight'
site.menu_style = 'default'

import dashboards

class BaseIndex(AppDashboard):
    app_label = 'base'
    #widget_customiz = False
    
site.register_appindex(BaseIndex)

import admins
import pages
