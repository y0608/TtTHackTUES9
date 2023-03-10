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

networkInterface = "wlp3s0"

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
        packet_info['src_addr']  = int(packet.ip.src.replace('.',''))             # source address
        packet_info['src_port']  = int(packet[packet.transport_layer].srcport)   # source port
        packet_info['src_mac']   = int(packet.eth.src.replace(':',''),16)         # source mac
        packet_info['dst_addr']  = int(packet.ip.dst.replace('.',''))             # destination address
        packet_info['dst_port']  = int(packet[packet.transport_layer].dstport)   # destination port
        packet_info['dst_mac']   = int(packet.eth.dst.replace(':',''),16)         # destination mac
        packet_info['size']      = len(packet)                                    # length of the packet
        packet_info['malicious'] = 0
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

def get_invalid_ips(mac):
    # get ips from the blacklist database
    pass
    #connection = sqlite3.connect('mydb.db')
    sql_select_Query = "select * from white_list"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    return records


def get_valid_ips(ip):
    # get ips from the whitelist database
    pass
    sql_select_Query = "select * from black_list"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    return records

def unblock_ip(ip):
    # unblock ip
    # remove from blacklist database if exists
    whitelist_ip(ip)
    pass

def block_ip(ip):
    # block ip
    # remove from whitelist database if exists
    blacklist_ip(ip)
    pass

def whitelist_ip(ip):
    # add ip to the whitelist database
    pass

    # connection = sqlite3.connect(
    # wldb_host, wldb_database, db_user, db_password)

    #Creating a cursor object using the cursor() method
    cursor = connection.cursor()
    # Preparing SQL query to INSERT a record into the database.
    sql = """"""

    # Executing the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    connection.commit()    

def blacklist_ip(ip):
    # add ip to the blacklist database
    pass

    connection = sqlite3.connect(
    wldb_host, wldb_database, db_user, db_password)

    #Creating a cursor object using the cursor() method
    cursor = connection.cursor()

    # Preparing SQL query to INSERT a record into the database.
    sql = """INSERT INTO EMPLOYEE(
    FIRST_NAME, LAST_NAME, AGE, SEX, INCOME)
    VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

    # Executing the SQL command
    cursor.execute(sql)

    # Commit your changes in the database
    connection.commit()

def IoT_to_Internet(source, destination):
    valid_ips = get_valid_ips(source)

    if 2 > valid_ips.len():
        whitelist_ip(destination)
        return

    if 1 > valid_ips.count(destination):
        block_ip(source)
        return

def Internet_to_IoT(source, destination):
    pass


        ##DATABASE##    
##############################
capture = pyshark.LiveCapture(interface='wlp3s0')
capture.sniff(timeout=10)
print("aaa")
strarts=load_file('file.txt')
for packet in capture:
    try:
        if cmp_mac_address_start(packet.eth.src,starts)==False:
            pass
    except AttributeError as e:
        pass
    
    row = make_dict(packet)
    #source, destination = get_source_and_destination(row)
    print(row)
    if row is None:
        pass
    source = row['src_addr']
    destination = row['dst_addr']
    #IoT_to_Internet(source, destination)
    #Internet_to_IoT(source, destination)
    csv_create(row)

############################
