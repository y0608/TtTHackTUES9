# RUN WITH SUDO

import os
import iptc
import pyshark
from Web.TtTsite.main.find_devices import get_devices
from .models import IotDevice, Whitelist, Blacklist

class Packet_t:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, protocol):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        

class Device_t:
    def __init__(self, wl = [], bl = [], name = ""):
        self.name = name
        self.wl = wl
        self.bl = bl

    def has_in_wl_protocol(self, protocol):
        for packet in self.wl:
            if packet.protocol == protocol:
                return True
        return False 

    def has_in_wl_src_ip(self, ip):
        for packet in self.wl:
            if packet.src_ip == ip:
                return True
        return False 
    
    def has_in_wl_dst_ip(self, ip):
        for packet in self.wl:
            if packet.dst_ip == ip:
                return True
        return False 

    def has_in_wl_src_port(self, port):
        for packet in self.wl:
            if packet.src_port == port:
                return True
        return False 
    
    def has_in_wl_dst_port(self, port):
        for packet in self.wl:
            if packet.dst_port == port:
                return True
        return False 

os.environ["XTABLES_LIBDIR"] = "/usr/lib/x86_64-linux-gnu/xtables"

_DEBUG_ = True

# Define the network interface
interface = "wlp0s20f3"
devices = dict()

# Define a function to block traffic from a specific IP address
def block_ip(ip_address, destination_ip):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    rule = iptc.Rule()
    rule.src = ip_address
    rule.dst = destination_ip
    rule.target = iptc.Target(rule, "REJECT")
    
    existing_rules = chain.rules
    for existing_rule in existing_rules:
        if existing_rule == rule:
            print("Rule already exists in chain")
            return
    
    chain.insert_rule(rule)

def unblock_ip(ip_address, destination_ip):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    rule = iptc.Rule()
    rule.src = ip_address
    rule.dst = destination_ip
    rule.target = iptc.Target(rule, "REJECT")

    existing_rules = chain.rules
    for existing_rule in existing_rules:
        if existing_rule == rule:
            chain.delete_rule(rule)
            return
    

def sniff_traffic():
    # Listen for incoming traffic on the specified interface
    capture = pyshark.LiveCapture(interface=interface)
    print("Listening for incoming traffic...")

    for packet in capture.sniff_continuously():

        # Check if the packet is not destined for the whitelisted IP address
        if "IP" in packet and packet.ip.dst in devices.keys():
            if not devices[packet.ip.dst].has_in_wl_dst_ip(packet.ip.src):
                if _DEBUG_:
                    print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
                if _DEBUG_:
                    print(f"Blocking traffic to ip: {packet.ip.src}")
                
                # Block traffic from the device
                # TODO: block packet.ipv6.dest if the device has an ipv6 address
                # block_ip(packet.ip.dst, packet.ip.src)
            if not devices[packet.ip.dst].has_in_wl_dst_port(packet.port.src):
                if _DEBUG_:
                    print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
                if _DEBUG_:
                    print(f"Blocking traffic to port: {packet.port.src}")
                
                # Block traffic from the device
                # TODO: block packet.ipv6.dest if the device has an ipv6 address
                # block_ip(packet.ip.dst, packet.ip.src)

            if not devices[packet.ip.dst].has_in_wl_dst_port(packet.port.src):
                if _DEBUG_:
                    print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
                if _DEBUG_:
                    print(f"Blocking traffic to port: {packet.port.src}")
                
                # Block traffic from the device
                # TODO: block packet.ipv6.dest if the device has an ipv6 address
                # block_ip(packet.ip.dst, packet.ip.src)
                
        elif "IPv6" in packet and packet.ipv6.dst in devices.keys():
            if not devices[packet.ipv6.dst].has_in_wl_dst_ip(packet.ipv6.src):
                if _DEBUG_:
                    print("Source: " + packet.ipv6.src + " -> " + packet.ipv6.dst) 
                    
                if _DEBUG_:
                    print(f"Blocking traffic to ip {packet.ipv6.src}")
                
            # Block traffic from the device
            # TODO: block packet.ipv6.dest if the device has an ipv6 address
            # block_ip(packet.ip.dst, packet.ip.src)

if __name__ == "__main__":
    # get devices
    devices = {}
    dbIot = IotDevice.objects.all()

    for device in dbIot:
        myDevice = Device_t(Whitelist.objects.filter(device=device.id),
                            Blacklist.objects.filter(device=device.id),
                            device.name)
        devices[device.ip] = myDevice
    # sniff the traffic

    sniff_traffic()