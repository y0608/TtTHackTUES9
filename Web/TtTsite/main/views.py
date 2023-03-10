from django.shortcuts import render
from django.http import HttpResponse
from .models import IotDevice, Whitelist, Blacklist

from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(response,id):
    device = IotDevice.objects.get(id=id)
    # whitelist = device.whitelist_set.all()
    # blacklist = device.blacklist_set.all()
    return render(response,"main/list.html",{"device":device})

def home(response):
    devices = IotDevice.objects.all()
    return render(response,"main/home.html",{"devices":devices})