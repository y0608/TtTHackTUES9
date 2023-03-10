import pyshark
import datetime
import sqlite3
import csv
import os

db_user = ''
db_password = ''

tdb_host = ''
tdb_database = ''

wldb_host = ''
wldb_database = ''

def load_file(file_name):
    starts = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line[:-1]
            starts.append(line)
    return starts

def cmp_mac_address_start(curr_mac_address, starts):
    for start in starts:
        if curr_mac_address == start:
            return True
    return False


def make_dict(packet):
    packet_info={}
    try:
        time = datetime.datetime.now()
        packet_info['localtime'] = time.year*10000000000 + time.month * 100000000 + time.day * 1000000 + time.hour*10000 + time.minute*100 + time.second
        packet_info['src_port']  = 1                                              # source port
        packet_info['src_mac']   = int(packet.eth.src.replace(':',''),16)         # source mac
        packet_info['dst_port']  = 1                                              # destination port
        packet_info['dst_mac']   = int(packet.eth.dst.replace(':',''),16)         # destination mac
        packet_info['size']      = len(packet)                                    # length of the packet
        packet_info['malicious'] = 0
        
        if 'TCP' in packet or 'UDP' in packet:
            packet_info['src_port']  = int(packet[packet.transport_layer].srcport)   # source port
            packet_info['dst_port']  = int(packet[packet.transport_layer].dstport)   # destination port

        if 'IP' in packet:
            print("asdf")
            packet_info['dst_addr']  = int(packet.ip.dst.replace('.',''))             # destination address
            packet_info['src_addr']  = int(packet.ip.src.replace('.',''))             # source address
        if 'IPv6' in packet:
            packet_info['dst_addr']  = int(packet.ip.dst.replace(':',''), 16)             # destination address
            packet_info['src_addr']  = int(packet.ip.src.replace(':',''), 16)             # source address

    except AttributeError as e:
        # ignore packets other than TCP, UDP and IPv4
        return None
    return packet_info

def csv_create(input):
    # create a csv file for the ML training
    pass
    # field names 
    fields = ['localtime','src_addr','src_port','src_mac','dst_addr','dst_port','dst_mac','size','malicious'] 
    with open('traffic.csv', 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        if os.path.getsize('traffic.csv')==0:
            writer.writeheader()
        writer.writerow(input)

connection = sqlite3.connect('mydb.db')

def get_invalid_ips(ip):
    # get ips from the blacklist database
    connection = sqlite3.connect('db.sqlite3')
    sql_select_Query = "SELECT main_blacklist.ip FROM main_blacklist LEFT JOIN main_iotdevice ON main_blacklist.device_id=main_iotdevice.id WHERE main_iotdevice.ip=?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    records = cursor.fetchall()
    connection.close()
    return records


def get_valid_ips(ip):
    # get ips from the whitelist database
    connection = sqlite3.connect('db.sqlite3')
    sql_select_Query = "SELECT main_whitelist.ip FROM main_whitelist LEFT JOIN main_iotdevice ON main_whitelist.device_id=main_iotdevice.id WHERE main_iotdevice.ip=?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    records = cursor.fetchall()
    connection.close()
    return records

def block_ip(ip):
    # remove from whitelist database if exists in future
    blacklist_ip(ip)
    pass 

def whitelist_ip(ip,add_ip):
    # add ip to the blacklist database
    connection = sqlite3.connect('db.sqlite3')
    sql_select_Query = "select main_iotdevice.id from main_iotdevice where main_iotdevice.ip==?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    device_id = cursor.fetchone()
    sql_insert_Query = "insert into main_whitelist(ip,device_id)values(?,?)"
    if device_id:
        cursor.execute(sql_insert_Query,(add_ip,device_id[0]))
        connection.commit()
    connection.close()

def blacklist_ip(ip,blocked_ip):
    # add ip to the blacklist database
    connection = sqlite3.connect('db.sqlite3')
    sql_select_Query = "select main_iotdevice.id from main_iotdevice where main_iotdevice.ip==?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    device_id = cursor.fetchone()
    sql_select_Query = "select main_whitelist.id from main_whitelist left join main_iotdevice on main_whitelist.device_id==main_iotdevice.id where main_iotdevice.ip==? and main_whitelist.ip==?"
    cursor.execute(sql_select_Query,(ip,blocked_ip))
    whitelist_ip= cursor.fetchone()
    if whitelist_ip:
        sql_delete_Query = "delete from main_whitelist where main_whitelist.id==?"
        cursor.execute(sql_delete_Query,(whitelist_ip[0],))
        connection.commit()
    sql_insert_Query = "insert into main_blacklist(ip,device_id)values(?,?)"
    if device_id:
        cursor.execute(sql_insert_Query,(blocked_ip,device_id[0]))
        connection.commit()
    connection.close()

def IoT_to_Internet(source, destination):
    valid_ips = get_valid_ips(source)

    if 2 > valid_ips.len():
        whitelist_ip(destination)
        return

    if 1 > valid_ips.count(destination):
        block_ip(source)
        return

def Internet_to_IoT(source, destination):
    valid_ips = get_valid_ips(destination)

    if 2 > valid_ips.len():
        whitelist_ip(source)
        return

    if 1 > valid_ips.count(source):
        block_ip(source)
        return


        ##DATABASE##    
##############################
#starts=load_file('mac_addresses.txt')
#rint(starts)
#records=get_valid_ips("192.12.24.2")
blacklist_ip("123.123.213.23","452.")
# capture = pyshark.LiveCapture(interface='wlan0')
# capture.sniff(timeout=10)
# print("aaa")

# for packet in capture:
#     if 'ETH Layer' in str(packet.layers) and ('IP' in packet or 'IPv6' in packet) and cmp_mac_address_start(packet.eth.src,starts):
#         print(packet)
#         row = make_dict(packet)
#         #source, destination = get_source_and_destination(row)
#         if row is None:
#             pass
#         #source = row['src_addr']
#         #destination = row['dst_addr']
#         #IoT_to_Internet(source, destination)
#         #Internet_to_IoT(source, destination)
#         csv_create(row)

############################


