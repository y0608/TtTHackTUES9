from django.shortcuts import render
from django.http import HttpResponse
from .models import IotDevice, Whitelist, Blacklist

from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def index(response,id):
    # device = IotDevice.objects.get(id=id)
    # return render(response,"main/list.html",{"device":device})
    device = IotDevice.objects.get(id=id)
 
    if response.method == "POST":
        if response.POST.get("newItemWhitelist"):
            txt = response.POST.get("new")    
            if len(txt) > 2:
                device.whitelist_set.create(ip=txt)
            else:
                print("invalid")
        elif response.POST.get("newItemBlacklist"):
            txt = response.POST.get("new")    
            if len(txt) > 2:
                device.blacklist_set.create(ip=txt)
            else:
                print("invalid")
               
        elif response.POST.get("moveToWhitelist"):
            print("AAAAAAAAA" + response.POST.get("moveToWhitelist"))
            # id = ...
            # tempip = 
            # device.blacklist_set.all()[id].delete()
            # device.blacklist_set.create(ip=tempip)

        elif response.POST.get("moveToBlacklist"):
            pass
            # id = ...
            # tempip = 
            # device.blacklist_set.all()[id].delete()# delete from whitelist
            # device.blacklist_set.create(ip=tempip)# add to blacklist
                              
    return render(response,"main/list.html",{"device":device})


def home(response):
    devices = IotDevice.objects.all()
    return render(response,"main/home.html",{"devices":devices})