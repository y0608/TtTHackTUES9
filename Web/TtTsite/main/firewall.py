# RUN WITH SUDO

import os
import iptc
import pyshark
# from find_devices import get_devices
# from .models import IotDevice, Whitelist, Blacklist
import sqlite3

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
    rule.target = iptc.Target(rule, "DROP")
    
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
    rule.target = iptc.Target(rule, "DROP")

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
        if "IP" in packet and packet.ip.src in devices.keys():
            if not devices[packet.ip.src].has_in_wl_dst_ip(packet.ip.dst):
                if _DEBUG_:
                    print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
                if _DEBUG_:
                    print(f"Blocking traffic to ip: {packet.ip.dst}")
                
                # Block traffic from the device
                # TODO: block packet.ipv6.dest if the device has an ipv6 address
                # block_ip(packet.ip.src, packet.ip.dst)
            # if not devices[packet.ip.dst].has_in_wl_dst_port(packet.port.src):
            #     if _DEBUG_:
            #         print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
            #     if _DEBUG_:
            #         print(f"Blocking traffic to port: {packet.port.src}")
                


                # Block traffic from the device
                # TODO: block packet.ipv6.dest if the device has an ipv6 address
                # block_ip(packet.ip.dst, packet.ip.src)

            # if not devices[packet.ip.dst].has_in_wl_dst_port(packet.port.src):
            #     if _DEBUG_:
            #         print("Source: " + packet.ip.src + " -> " + packet.ip.dst) 
                
            #     if _DEBUG_:
            #         print(f"Blocking traffic to port: {packet.port.src}")
                
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
            # block_ip(packet.ipv6.dst, packet.ipv6.src)


def stringToPacket(str):
    packets=[]
    for s in str:
        packets.append(Packet_t(s[1],s[2],s[3],s[4],s[5],s[6]))
    return packets

if __name__ == "__main__":
    # get devices
    # connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    # connection = sqlite3.connect('/home/yoan/Documents/Programming/Projects/TtTHackTUES9/Web/TtTsite/db.sqlite3')

    # connection = sqlite3.connect('db.sqlite3')
    connection = sqlite3.connect('/home/yoan/Documents/Programming/Projects/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    
    sql_select_Query = "select * from main_iotdevice"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    devicesFetch = cursor.fetchall()
    for d in devicesFetch:
        sql_select_Query="select * from main_whitelist where ? = main_whitelist.device_id"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(d[2],))
        white_list = cursor.fetchall()
        sql_select_Query="select * from main_blacklist where ? = main_blacklist.device_id"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query,(d[2],))
        black_list = cursor.fetchall()
        devices[d[2]] = Device_t(stringToPacket(white_list), stringToPacket(black_list), d[1])
    connection.close()
    
    sniff_traffic()
    # block_ip("192.168.1.21", "192.168.1.22")