from django.contrib import admin
from localapp .models import Printerdata,Scannerdata,LocalappLoginmodel,LocalseverHistory,Localapp_Register,Local_UserrolePermissions
# Register your models here.
admin.site.register(Printerdata)
admin.site.register(Scannerdata)
admin.site.register(LocalappLoginmodel)
admin.site.register(LocalseverHistory)
admin.site.register(Localapp_Register)
admin.site.register(Local_UserrolePermissions)