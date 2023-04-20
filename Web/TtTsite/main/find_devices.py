import pyshark
import ast
import json
import os
from .models import IotDevice, Whitelist, Blacklist


class Packet_t:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, protocol):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol


class Device_t:
    def __init__(self, wl=[], bl=[], name=""):
        self.name = name
        self.wl = wl
        self.bl = bl


devicesPath = "./main/devices.txt"
macPath = "./main/iot_devices_mac_addresses.txt"

# Define the network interface
interface = "wlp2s0"


def file_to_dict(filename):
    result = dict()
    with open(filename, 'r') as f:
        s = f.read()
        result = ast.literal_eval(s)

    return result


def dict_to_file(d):
    with open(devicesPath, 'w') as devices:
        devices.write(json.dumps(d))


def cmp_mac_address_start(curr_mac_address):
    with open(macPath, 'r') as file:
        for mac_address_line in file:
            if curr_mac_address.startswith(mac_address_line[:-1]):
                return True
    return False


def get_devices(perm_1=True, perm_2=True, perm_3=True):
    # TESTING ONLY: REMOVE
    # devices = file_to_dict(devicesPath) # django runs scripts inside TtTsite
    # return devices

    # scan for devices
    capture = pyshark.LiveCapture(interface=interface)
    timer = 400  # how many iterations before program breaks

    # {src_ip:Device_t}
    devices = {}
    dbIot = IotDevice.objects.all()

    for device in dbIot:
        myDevice = Device_t(Whitelist.objects.filter(device=device.id),
                            Blacklist.objects.filter(device=device.id),
                            device.name)
        devices[device.ip] = myDevice

    # add the first five ip destination addresses
    for packet in capture.sniff_continuously():
        # perm_1,2,3 are the different filters
        # if perm_3 and packet.size > 1024:
        #     return

        # if perm_2:
        #     if all_have_more_than_5():
        #         return

        # if in ethernet layer
        if 'ETH Layer' in str(packet.layers):
            # if current device is IoT device
            if (cmp_mac_address_start(packet.eth.src)):
                # if device is in devices
                if packet.ip.src not in devices.keys():
                    if perm_2:  # check if they are max 5 addresses(packets)
                        if devices[packet.ip.src].wl < 5:
                            myNewPacket = Packet_t(
                                packet.ip.src, packet.ip.dst, packet.ip.src_port,
                                packet.ip.dst_port, packet.ip.proto)
                            devices[packet.ip.src].wl.append(myNewPacket)

                            newWl = Whitelist(device=Whitelist.filter(src_ip=packet.ip.src)[0].device, src_ip=myNewPacket.src_ip,
                                              dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                                              dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol)
                            newWl.save()
                    else:
                        myNewPacket = Packet_t(
                            packet.ip.src, packet.ip.dst, packet.ip.src_port,
                            packet.ip.dst_port, packet.ip.proto)
                        devices[packet.ip.src].wl.append(myNewPacket)

                        newWl = Whitelist(device=Whitelist.filter(src_ip=packet.ip.src)[0].device, src_ip=myNewPacket.src_ip,
                                          dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                                          dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol)
                        newWl.save()
                    pass
                print(f"Added {packet.ip.dst} to {packet.ip.src}")

        timer -= 1
        if perm_1 and timer == 0:
            return
