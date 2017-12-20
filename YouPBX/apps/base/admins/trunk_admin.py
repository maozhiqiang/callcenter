# coding=utf-8

from xadmin import site
from xadmin.utils import fa_icon

from apps.base import models
from apps.common import ReXmlAdmin

class TrunkRoutePatternInline(object):
    model = models.TrunkRoutePattern
    extra = 0


class TrunkAdmin(ReXmlAdmin):
    
    inlines = [ TrunkRoutePatternInline ]
    menu_group = 'trunk_group'
    order = 2
    model_icon = fa_icon('cogs')

site.register(models.Trunk, TrunkAdmin)
