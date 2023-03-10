from django.contrib import admin
from .models import IotDevice, Whitelist, Blacklist
# Register your models here.

admin.site.register(IotDevice)
admin.site.register(Whitelist)
admin.site.register(Blacklist)
