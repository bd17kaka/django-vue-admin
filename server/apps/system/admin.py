from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import User, Organization, Role, Permission, DictType, Dict, File, Measurement, Dataset
# Register your models here.
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(DictType)
admin.site.register(Dict, SimpleHistoryAdmin)
admin.site.register(File)
admin.site.register(Measurement)
admin.site.register(Dataset)