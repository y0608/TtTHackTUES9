import pyshark

#   Program for fainding the mac addresses of iot devices. 
#   The program tracks the trafic in a network and compare the mac
#   addresses of devices that generates trafic. If a mach is found 
#   the program writes it.

def load_file(file_name):
    starts = []
    with open(file_name, 'r') as file:
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
    capture = pyshark.LiveCapture(interface = 'wlp2s0')
    capture.sniff(timeout = 10)
    starts = load_file("esp2.txt") #load the starts of mac addresses we want to track
    mac_address = load_file("mac_addresses.txt") #load mac addresses we already added in the data base( no need to be added again )
    timer = 400 #how many iterations before program breaks

    for packet in capture:
        if 'ETH Layer' in str(packet.layers):
            mac_addr = packet.eth.src

            if mac_addr not in mac_address and cmp_mac_address_start(mac_addr, starts):
                mac_address.append(mac_addr)    
                print("new mac address added: ", mac_addr)
                with open("mac_addresses.txt", 'a') as f:
                    f.write(mac_addr + '\n') #add the new mac address in the text file ( not to be added again )
            
            print(mac_addr + " " + str(timer))
        
        timer -= 1
        if timer == 0:
            return
            

get_all_mac_addresses()
