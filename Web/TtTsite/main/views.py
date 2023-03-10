from django.shortcuts import render
from django.http import HttpResponse
from .models import IotDevice, Whitelist, Blacklist
# Create your views here.

def index(response,id):
    devices = IotDevice.objects.get(id=id)
    whitelist = devices.whitelist_set.all()
    blacklist = devices.blacklist_set.all()
    return HttpResponse("<h1>%s</h1>" % blacklist[0])