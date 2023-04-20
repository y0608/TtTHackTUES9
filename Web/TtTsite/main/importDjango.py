from django.shortcuts import render
from django.http import HttpResponse
from .models import IotDevice, Whitelist, Blacklist

from django.shortcuts import render
from django.urls import reverse


device = IotDevice(name="asdfasdf",ip="1201.1")
device.save()