from django.db import models

# Create your models here.


class IotDevice(models.Model):
    name = models.CharField(max_length=200)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Whitelist(models.Model):
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)
    src_ip = models.CharField(max_length=100)
    dst_ip = models.CharField(max_length=100)
    src_port = models.CharField(max_length=100)
    dst_port = models.CharField(max_length=100)
    protocol = models.CharField(max_length=100)

    def __str__(self):
        return self.dst_ip

class Blacklist(models.Model):
    device = models.ForeignKey(IotDevice, on_delete=models.CASCADE)
    src_ip = models.CharField(max_length=100)
    dst_ip = models.CharField(max_length=100)
    src_port = models.CharField(max_length=100)
    dst_port = models.CharField(max_length=100)
    protocol = models.CharField(max_length=100)

    def __str__(self):
        return self.dst_ip
