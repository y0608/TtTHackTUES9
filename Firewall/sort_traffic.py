import pyshark
import time
import sqlite3

# define interface
networkInterface = "wlp3s0"

# define capture object
capture = pyshark.LiveCapture(interface=networkInterface)

print("listening on %s" % networkInterface)

packet_info={
    'localtime' : None,
    'protocol'  : None,
    'src_addr'  : None,
    'src_port'  : None,
    'src_mac'   : None,
    'dst_addr'  : None,
    'dst_port'  : None,
    'dst_mac'   : None,
    'size'      : None,
    'malicious' : 0 
}
columns = ', '.join(packet_info.keys())

db = sqlite3.connect('mydb.db')

db.execute(f'CREATE TABLE IF NOT EXISTS mytable ({columns})')

for packet in capture.sniff_continuously(packet_count=10):
    # adjusted output
    try:
        # get timestamp
        packet_info['localtime'] = time.asctime(time.localtime(time.time()))
     
        # get packet content
        packet_info['protocol'] = packet.transport_layer                    # protocol type
        packet_info['src_addr'] = packet.ip.src                             # source address
        packet_info['src_port'] = packet[packet_info['protocol']].srcport   # source port
        packet_info['src_mac']  = packet.eth.src                            # source mac
        packet_info['dst_addr'] = packet.ip.dst                             # destination address
        packet_info['dst_port'] = packet[packet_info['protocol']].dstport   # destination port
        packet_info['dst_mac']  = packet.eth.dst                            # destination mac
        packet_info['size']     = len(packet)                               # length of the packet
        
        values_placeholder = ', '.join(['?'] * len(packet_info))

        #for key,value in packet_info.items():
        db.execute(f'INSERT INTO mytable ({columns}) VALUES ({values_placeholder})', tuple(packet_info.values()))
        db.commit()

        # output packet info
        print(packet_info)
        #print ("%s IP %s:%s mac %s<->IP %s:%s mac %s (%s) size:%d" % (localtime, src_addr, src_port,src_mac, dst_addr, dst_port,dst_mac, protocol,size))
    except AttributeError as e:
        # ignore packets other than TCP, UDP and IPv4
        pass
   # db.close()
    print (" ")