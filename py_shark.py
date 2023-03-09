import pyshark
import numpy as np


def load_file():
    starts = []
    with open('esp2.txt', 'r') as file:
        for line in file:
            line = line[:-1]
            starts.append(line)

    return starts


def cmp_mac_address_start(curr_mac_address, starts):
    for start in starts:
        if curr_mac_address.startswith(start):
            return True
    return False

def get_all_mac_addresses():
    capture = pyshark.LiveCapture(interface='wlp2s0',output_file="pyshark.pcap")
    capture.sniff(timeout=10)
    
    starts = load_file()
    mac_address = []
    for packet in capture:
        if 'ETH Layer' in str(capture[0].layers) and 'ETH Layer' in str(packet.layers):
            if(packet.eth.src not in mac_address and cmp_mac_address_start(packet.eth.src, starts)):
                mac_address.append(packet.eth.src)
                print("new mac address added: ", packet.eth.src)
            print(packet.eth.src)        

get_all_mac_addresses()

