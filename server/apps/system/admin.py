from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import User, Organization, Role, Permission, DictType, Dict, File, Task, solution, Dataset, Measurement
# Register your models here.
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(DictType)
admin.site.register(Dict, SimpleHistoryAdmin)
admin.site.register(File)
admin.site.register(Task)
admin.site.register(solution)
admin.site.register(Dataset)
admin.site.register(Measurement)