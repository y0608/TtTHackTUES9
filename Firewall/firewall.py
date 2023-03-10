import pyshark
import datetime
import sqlite3
import csv
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase


def send_mail(src_ip, dst_ip):

    receiver_list = ['victorhandzhiev@gmail.com']
    body = """
    Source IP(blocked): {}

    Destination IP: {}


    """.format(src_ip, dst_ip)
    for receiver in receiver_list:
        msg = MIMEMultipart()
        msg['From'] = 'IoT Firewall'
        msg['To'] = receiver
        msg['Subject'] = 'New security issue detected!'

        msg.attach(MIMEText('{}'.format(body), 'plain', 'utf-8'))

        text = msg.as_string()
        mail_server.sendmail("hacktues9TtT@gmail.com", receiver, text)

# SMTP setup
port = 465  # For SSL
# password = getpass(prompt="Type your password and press enter: ", stream=None)
password = "byuaykowxvwoepil"
context = ssl.create_default_context()
mail_server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
mail_server.connect("smtp.gmail.com", port)
mail_server.ehlo()
mail_server.login("hacktues9TtT@gmail.com", password)


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
        block_ip(blocked_ip)
    connection.close()

def IoT_to_Internet(source, destination):
    valid_ips = get_valid_ips(source)
    invalid_ips = get_invalid_ips(source)
    for i in invalid_ips:
        if destination in i:
            return
        
    if 2 > len(valid_ips):
        whitelist_ip(destination)
        return

    if 1 > valid_ips.count(destination):
        send_mail(source, destination)
        mail_server.quit()
        #blacklist_ip(source,destination)
        return

def Internet_to_IoT(source, destination):
    valid_ips = get_valid_ips(destination)
    invalid_ips = get_invalid_ips(destination)
    for i in invalid_ips:
        if source in i:
            return
        
    if 2 > len(valid_ips):
        whitelist_ip(source)
        return
    
    if 1 > valid_ips.count(source):
        send_mail(source, destination)
        mail_server.quit()
        blacklist_ip(destination,source)
        return


        ##DATABASE##    
##############################
starts=load_file('mac_addresses.txt')
capture = pyshark.LiveCapture(interface='wlan0')
capture.sniff(timeout=10)
print("aaa")
for packet in capture:
    src = cmp_mac_address_start(packet.eth.src,starts)
    dst = cmp_mac_address_start(packet.eth.dst,starts)
    if 'ETH Layer' in str(packet.layers) and ('IP' in packet or 'IPv6' in packet) and (src or dst):
        row = make_dict(packet)
        if row is None:
            pass
        source = row['src_addr']
        destination = row['dst_addr']
        if src:
            IoT_to_Internet(source, destination)
        if dst:
            Internet_to_IoT(source, destination)
        csv_create(row)

############################byuaykowxvwoepil


