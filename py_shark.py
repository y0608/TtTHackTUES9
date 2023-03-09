import pyshark


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
    capture = pyshark.LiveCapture(interface='wlp2s0')
    capture.sniff(timeout=10)
    macaddresses = {}
    starts = load_file()
    mac_address = []
    names = "" 
    values = ""
    
    for packet in capture:
        if 'ETH Layer' in str(packet.layers):
            
            if packet.eth.src not in mac_address:
                if cmp_mac_address_start(packet.eth.src, starts):
                    mac_address.append(packet.eth.src)
                    print("new mac address added: ", packet.eth.src)
            
            if(packet.eth.src in mac_address):
                print("in")
                print(packet)
                if packet.eth.src not in macaddresses:
                    macaddresses[packet.eth.src]=[]
                
                macaddresses[packet.eth.src].append({})
                
                if len(macaddresses[packet.eth.src])>25:
                    macaddresses[packet.eth.src].pop(0)
                
                if 'IP' in packet:
                    print("IP")
                    names = packet.ip._all_fields
                    values = packet.ip._all_fields.values()
                
                if 'IPv6' in packet:
                    print("IPv6")
                    names = packet.ipv6._all_fields
                    values = packet.ipv6._all_fields.values()
                
                print(macaddresses[packet.eth.src][0])

                for n,v in zip(names, values):
                    macaddresses[packet.eth.src][len(macaddresses[packet.eth.src])-1][n] = v
                    print(macaddresses[packet.eth.src][len(macaddresses[packet.eth.src])-1][n])

            print(packet.eth.src)

get_all_mac_addresses()

