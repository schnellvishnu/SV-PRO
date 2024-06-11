
from django.contrib import admin
from serverdataapp .models import ServerPrinterdata,ServerScannerdata

# Register your models here.
admin.site.register(ServerPrinterdata)
admin.site.register(ServerScannerdata)