from django.shortcuts import render
from django.http import HttpResponse
from .models import IotDevice, Whitelist, Blacklist

from django.shortcuts import render
from django.urls import reverse

# Create your views here.

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
                device.whitelist_set.create(ip=txt)
            else:
                print("invalid")
        elif response.POST.get("newItemBlacklist"):
            txt = response.POST.get("new")    
            if len(txt) > 2:
                device.blacklist_set.create(ip=txt)
            else:
                print("invalid")
                      
        elif response.POST.get("whiteToBlacklist"):            
            id = int(response.POST.get("whiteToBlacklist"))
            currentDevice = device.whitelist_set.all().filter(id=id)
            tempip = currentDevice[0].ip
            currentDevice.delete()
            device.blacklist_set.create(ip=tempip)
            
        elif response.POST.get("blackToWhitelist"):
            id = int(response.POST.get("blackToWhitelist"))
            currentDevice = device.blacklist_set.all().filter(id=id)
            tempip = currentDevice[0].ip
            currentDevice.delete()
            device.whitelist_set.create(ip=tempip)
            
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
            
    return render(response,"main/list.html",{"device":device})


def home(response):
    devices = IotDevice.objects.all()
    
    if response.method == "POST":
        if response.POST.get("getDevices"):
            print("Getting devices")
            
            #TODO: add path that is only in the project ("../../../Firewall/mac_addresses.txt")
            macAddresses = load_file("/home/yoan/Documents/Programming/ProgrammingSchool/11grade/TtTHackTUES9/Firewall/mac_addresses.txt")
            
            # devices.delete()
            # for macAddress in macAddresses:
            #     newDevice = IotDevice(name="blank name",mac=macAddress,ip="blank ip")
            #     newDevice.save()
                    
            ## if we want to only add new devices
            for macAddress in macAddresses:
                if(macAddress == ''):
                    continue
                
                newDevice = IotDevice(name="blank name",mac=macAddress,ip="blank ip")
                # save only if not saved yet
                shouldSave = True
                for device in devices:
                    if newDevice.name == device.name :
                        shouldSave = False
                if(shouldSave):
                    newDevice.save()
                    
        elif response.POST.get("removeDevice"):
            print("removeDevice")
            id = int(response.POST.get("removeDevice"))
            currentDevice = IotDevice.objects.get(id=id)
            currentDevice.delete()
                    
    return render(response,"main/home.html",{"devices":devices})