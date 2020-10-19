from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import User, Organization, Role, Permission, DictType, Dict, File

# Register your models here.
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(DictType)
admin.site.register(Dict, SimpleHistoryAdmin)
admin.site.register(File)

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE

class MoniterLog(admin.ModelAdmin):
    #dt_utc = datetime.datetime.strptime('action_time', '%Y-%m-%d %H:%M:%S')
    #str_utc = 'action_time'
    #dt_utc = datetime.datetime.strptime(str_utc, '%Y-%m-%d %H:%M:%S')
    #dt_jst =  dt_utc + datetime.timedelta(0,3600)
    #str_jst = dt_jst.strftime('%Y/%m/%d %H:%M:%S') 
    list_display = ('action_time','user','content_type','object_repr','change_message','action_flag')
    list_filter = ['action_time','user','content_type']
    ordering = ('-action_time',)

admin.site.register(LogEntry, MoniterLog)