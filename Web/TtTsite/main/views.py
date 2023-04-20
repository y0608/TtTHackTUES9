from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import reverse

from .models import IotDevice, Whitelist, Blacklist
from .find_devices import get_devices

# Create your views here.

option1 = True
option2 = True
option3 = True

def load_file(file_name):
    starts = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line[:-1]
            starts.append(line)
    return starts


def index(response,id):
    device = IotDevice.objects.get(id=id)
 
    if response.method == "POST":
        if response.POST.get("newItemWhitelist"):
            txt = response.POST.get("new")    
            if len(txt) > 2:
                device.whitelist_set.create(dst_ip=txt)
            else:
                print("invalid")
        elif response.POST.get("newItemBlacklist"):
            #TODO: провери дали го има в whitelist
            txt = response.POST.get("new")    
            if len(txt) > 2:
                device.blacklist_set.create(dst_ip=txt)
            else:
                print("invalid")
                      
        elif response.POST.get("whiteToBlacklist"):            
            id = int(response.POST.get("whiteToBlacklist"))
            currentDevice = device.whitelist_set.all().filter(id=id)
            tempip = currentDevice[0].dst_ip
            currentDevice.delete()
            device.blacklist_set.create(dst_ip=tempip)
            
        elif response.POST.get("blackToWhitelist"):
            id = int(response.POST.get("blackToWhitelist"))
            currentDevice = device.blacklist_set.all().filter(id=id)
            tempip = currentDevice[0].dst_ip
            currentDevice.delete()
            device.whitelist_set.create(dst_ip=tempip)
            
        elif response.POST.get("removeFromWhiteList"):
            print("remove from whitelist")
            id = int(response.POST.get("removeFromWhiteList"))
            currentDevice = device.whitelist_set.all().filter(id=id)
            currentDevice.delete()
            
        elif response.POST.get("removeFromBlackList"):
            print("removeFromBlackList")
            id = int(response.POST.get("removeFromBlackList"))
            currentDevice = device.blacklist_set.all().filter(id=id)
            currentDevice.delete()
        
        #TODO: make this button:
        # elif response.POST.get("removeAllFromBlackList"):
        #     print("removeAllFromBlackList")
        #     id = int(response.POST.get("removeAllFromBlackList"))
        #     currentDevice = device.blacklist_set.all().filter(id=id)
        #     currentDevice.delete()    
            
    return render(response,"main/list.html",{"device":device})


def home(response):
    devices = IotDevice.objects.all()
    
    if response.method == "POST":
        if response.POST.get("getDevices"):
            print("Getting devices")
            get_devices(option1,option2,option3)
                    
        elif response.POST.get("removeDevice"):
            print("removeDevice")
            id = int(response.POST.get("removeDevice"))
            currentDevice = IotDevice.objects.get(id=id)
            currentDevice.delete()
                    
    return render(response,"main/home.html",{"devices":devices})

def settings(request):
    # TODO: rename and set perm1, perm2, perm3
    global option1, option2, option3
    checkboxes = [{"name":"Packet count", "enabled": option1},
                  {"name":"Max 5 whitelisted", "enabled": option2},
                  {"name":"Packet size", "enabled": option3}]
    if request.method == "POST":
        options = request.POST.getlist("options")
        if(options.__contains__("Packet count")):
            option1 = True
        else:
            option1 = False
            
        if(options.__contains__("Max 5 whitelisted")):
            option2 = True
        else:
            option2 = False
            
        if(options.__contains__("Packet size")):
            option3 = True
        else:
            option3 = False
        print(option1,option2,option3)
        return redirect("/")
    return render(request,"main/settings.html",{"options":checkboxes})    