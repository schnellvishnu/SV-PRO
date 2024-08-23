
from django.contrib import admin
from serverdataapp .models import ServerPrinterdata,ServerScannerdata,ServerHistory,BackupScannerdata,BackupHistory

# Register your models here.
admin.site.register(ServerPrinterdata)
admin.site.register(ServerScannerdata)
admin.site.register(ServerHistory)
admin.site.register(BackupScannerdata)
admin.site.register(BackupHistory)