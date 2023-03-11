from django.db import models

# Create your models here.


class IotDevice(models.Model):
    name = models.CharField(max_length=200)
    mac = models.CharField(max_length=100)  # 17
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.name


#TODO:add a date and time column to whitelist and blacklist
class Whitelist(models.Model):
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip

class Blacklist(models.Model):
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip
