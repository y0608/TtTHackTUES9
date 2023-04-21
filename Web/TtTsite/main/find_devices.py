import pyshark
import ast
import json
import os
from models import IotDevice, Whitelist, Blacklist

class Packet_t:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, protocol, size):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        self.size = size

class Device_t:
    def __init__(self, wl=[], bl=[], name=""):
        self.name = name
        self.wl = wl
        self.bl = bl


devicesPath = "./main/devices.txt"
macPath = "./main/iot_devices_mac_addresses.txt"

# Define the network interface
interface = "wlp0s20f3"


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

def all_have_more_than_5(devices): 
    for d in devices.values():
        if len(d.wl)<5:
            return False
    return True

def size_filter(device,size):
    biggest=device.wl[0].size
    smallest=device.wl[0].size
    if len(device.wl)<2:
        return False
    for l in device.wl:
        if biggest<l.size:
            biggest=l.size
        if smallest>l.size:
            smallest=l.size
    if size>=smallest and size<=biggest:
        return False
    return True

def get_devices(perm_1=True, perm_2=True, perm_3=False):
    # TESTING ONLY: REMOVE
    # devices = file_to_dict(devicesPath) # django runs scripts inside TtTsite
    # return devices

    # scan for devices
    capture = pyshark.LiveCapture(interface=interface)
    timer = 4000  # how many iterations before program breaks

    # {src_ip:Device_t}
    devices = {}
    dbIot = IotDevice.objects.all()

    for device in dbIot:
        wl = []
        bl = []

        for p in device.whitelist_set.all():
            wl.append(Packet_t (p.src_ip, p.dst_ip, p.src_port, p.dst_port, p.protocol, p.size))

        for p in device.blacklist_set.all():
            bl.append(Packet_t (p.src_ip, p.dst_ip, p.src_port, p.dst_port, p.protocol, p.size))

        myDevice = Device_t(wl, bl, device.name)
        
        devices[device.ip] = myDevice

    # add the first five ip destination addresses
    for packet in capture.sniff_continuously():
        # perm_1,2,3 are the different filters
        # if perm_3 and packet.size > 1024:
        #     return
        if perm_2 and len(devices.values()) != 0:
             if all_have_more_than_5(devices):
                return
             

        if 'IP' in packet:
            ip_src=packet.ip.src
            ip_dst=packet.ip.dst
            proto=packet.ip.proto
            if "tcp" in packet:
                src_port=packet.tcp.srcport
                dst_port=packet.tcp.dstport
            elif "udp" in packet:
                src_port=packet.udp.srcport
                dst_port=packet.udp.dstport
        elif 'IPv6' in packet:
            ip_src=packet.ipv6.src
            ip_dst=packet.ipv6.dst
            #proto=packet.ipv6.proto
            proto = ''
            if "tcp" in packet:
                src_port=packet.tcp.srcport
                dst_port=packet.tcp.dstport
            elif "udp" in packet:
                src_port=packet.udp.srcport
                dst_port=packet.udp.dstport
        if perm_3:
            if size_filter(devices[ip_src],len(str(packet))):
                continue
        # if in ethernet layer
        # if 'ETH Layer' in str(packet.layers):
        if 'ETH' in packet:
            # if current device is IoT device
            if (cmp_mac_address_start(packet.eth.src)):
                if "IP" in packet and packet.ip.proto == "ICMP":
                    print("1: "+ packet.eth.src + " " + packet.ip.src + " " + packet.ip.dst)
                print("crma: " + packet.eth.src)
                # if device is in devices
                print("4")
                if ip_src not in devices.keys():
                    devices[ip_src] = Device_t()
                    new_device = IotDevice(name='', ip=ip_src)
                    new_device.save()
                    print("not in device")
                else:
                    try:
                        print("alo if")
                        if Whitelist.objects.filter(src_ip=ip_src, dst_ip=ip_dst)[0].device.ip == packet.ip.src:
                            continue
                    except:
                        print("catch")
                    
                if perm_2:  # check if they are max 5 addresses(packets)
                    # if ip_src not in devices.keys():
                    # devices[ip_src] = []
                    if len(devices[ip_src].wl) < 5:
                        myNewPacket = Packet_t(
                            ip_src, ip_dst, src_port,
                            dst_port, proto,len(str(packet)) )
                        devices[ip_src].wl.append(myNewPacket)

                        newWl = Whitelist(device=IotDevice.objects.filter(ip=ip_src)[0], src_ip = ip_src,
                                        dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                                        dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol, size= myNewPacket.size)
                        newWl.save()
                        # new_device.whitelist_set.create(src_ip = ip_src,
                        #                 dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                        #                 dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol, size= myNewPacket.size)
                else:
                    myNewPacket = Packet_t(
                        ip_src, ip_dst, src_port,
                        dst_port, proto,len(str(packet)))
                    devices[ip_src].wl.append(myNewPacket)

                    newWl = Whitelist(device=IotDevice.objects.filter(ip=ip_src)[0], src_ip = ip_src,
                                    dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                                    dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol,size= myNewPacket.size)
                    newWl.save()
                    # new_device.whitelist_set.create(src_ip = ip_src,
                    #                     dst_ip=myNewPacket.dst_ip, src_port=myNewPacket.src_port,
                    #                     dst_port=myNewPacket.dst_port, protocol=myNewPacket.protocol, size= myNewPacket.size)
                    
                print(f"Added {ip_dst} to {ip_src}")
        timer -= 1
        if perm_1 and timer == 0:
            return