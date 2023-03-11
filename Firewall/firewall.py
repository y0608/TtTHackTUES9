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
import subprocess
import sys

# SMTP setup
port = 465  # For SSL
# password = getpass(prompt="Type your password and press enter: ", stream=None)
password = "byuaykowxvwoepil"
context = ssl.create_default_context()
mail_server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
mail_server.connect("smtp.gmail.com", port)
mail_server.ehlo()
mail_server.login("hacktues9TtT@gmail.com", password)



def send_mail(src_ip, dst_ip):
    
    connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    sql_select_Query = "SELECT auth_user.email FROM auth_user"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    connection.close()
    receiver_list = [str(records[0]).replace(',','').replace('(','').replace(')','').replace("'",'')]
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
        packet_info['src_mac']   = packet.eth.src         # source mac
        packet_info['dst_port']  = 1                                              # destination port
        packet_info['dst_mac']   = packet.eth.dst         # destination mac
        packet_info['size']      = len(packet)                                    # length of the packet
        packet_info['malicious'] = 0
        
        if 'TCP' in packet or 'UDP' in packet:
            packet_info['src_port']  = packet[packet.transport_layer].srcport   # source port
            packet_info['dst_port']  = packet[packet.transport_layer].dstport   # destination port

        if 'IP' in packet:
            print("asdf")
            packet_info['dst_addr']  = packet.ip.dst             # destination address
            packet_info['src_addr']  = packet.ip.src             # source address
        if 'IPv6' in packet:
            packet_info['dst_addr']  = packet.ip.dst             # destination address
            packet_info['src_addr']  = packet.ip.src             # source address

    except AttributeError as e:
        # ignore packets other than TCP, UDP and IPv4
        return None
    return packet_info

def csv_create(input):
    # create a csv file for the ML training
    pass
    # field names 
    packet_info={}
    packet_info['localtime'] = input['localtime']
    packet_info['src_port']  = int(input['src_port'])                                      # source port
    packet_info['src_mac']   = int(input['src_mac'].replace(':',''),16)         # source mac
    packet_info['dst_port']  = int(input['dst_port'])                                              # destination port
    packet_info['dst_mac']   = int(input['dst_mac'].replace(':',''),16)         # destination mac
    packet_info['size']      = input['size']                                    # length of the packet
    packet_info['malicious'] = 0
#IPv4
    if '.' in input['dst_addr']:
        packet_info['dst_addr']  = int(input['dst_addr'].replace('.',''))             # destination address
        packet_info['src_addr']  = int(input['src_addr'].replace('.',''))             # source address
#IPv6   
    if ':' in input['dst_addr']:
        packet_info['dst_addr']  = int(input['dst_addr'].replace(':',''), 16)             # destination address
        packet_info['src_addr']  = int(input['src_addr'].replace(':',''), 16)  
    fields = ['localtime','src_addr','src_port','src_mac','dst_addr','dst_port','dst_mac','size','malicious'] 
    with open('traffic.csv', 'a', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        if os.path.getsize('traffic.csv')==0:
            writer.writeheader()
        writer.writerow(packet_info)

#connection = sqlite3.connect('mydb.db')

def get_invalid_ips(ip):
    # get ips from the blacklist database
    connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    sql_select_Query = "SELECT main_blacklist.ip FROM main_blacklist LEFT JOIN main_iotdevice ON main_blacklist.device_id=main_iotdevice.id WHERE main_iotdevice.ip=?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    records = cursor.fetchall()
    connection.close()
    return records


def get_valid_ips(ip):
    # get ips from the whitelist database
    connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    sql_select_Query = "SELECT main_whitelist.ip FROM main_whitelist LEFT JOIN main_iotdevice ON main_whitelist.device_id=main_iotdevice.id WHERE main_iotdevice.ip=?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    records = cursor.fetchall()
    connection.close()
    return records

def block_ip(ip):
    # remove from whitelist database if exists in future
    command = "iptables -A drop_blocked_lan_ip -i wlan0 -s " + ip + " -j DROP"
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)

def unblock_ip(ip):
    # remove from whitelist database if exists in future
    command = "iptables -D drop_blocked_lan_ip -i wlan0 -s " + ip + " -j DROP"
    subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    whitelist_ip(ip)

def whitelist_ip(ip,add_ip):
    # add ip to the blacklist database
  #  print("whitelist enter")
    connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
    sql_select_Query = "select main_iotdevice.id from main_iotdevice where main_iotdevice.ip==?"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query, (ip,))
    device_id = cursor.fetchone()
    sql_insert_Query = "insert into main_whitelist(ip,device_id)values(?,?)"
    if device_id:
 #       print("whitelist if enter")
        cursor.execute(sql_insert_Query,(add_ip,device_id[0]))
        connection.commit()
    connection.close()

def blacklist_ip(ip,blocked_ip):
    # add ip to the blacklist database
    connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
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
    invalid_ips = get_invalid_ips(source)
    for i in invalid_ips:
        if destination in i:
            return
    for i in valid_ips:
        if destination in i:
            return
    if 2 > len(valid_ips):
        whitelist_ip(source, destination)
        return

    if 1 > valid_ips.count(destination):
        send_mail(source, destination)
        #block_ip(source)
        blacklist_ip(source,destination)
        return

def Internet_to_IoT(source, destination):
    valid_ips = get_valid_ips(destination)
    invalid_ips = get_invalid_ips(destination)
    for i in invalid_ips:
        if source in i:
            return
    for i in valid_ips:
        if source in i:
            return
    if 2 > len(valid_ips):
        whitelist_ip(destination, source)
        return
    
    if 1 > valid_ips.count(source):
        send_mail(source, destination)
        blacklist_ip(destination,source)
        #block_ip(source)
        return

        ##DATABASE##    
##############################

capture = pyshark.LiveCapture(interface='wlan0')
capture.sniff(timeout=10)
print("aaa")
#send_mail("aaaa","aaaaa")
blocked=False
for packet in capture:
    starts=load_file('mac_addresses.txt')
    src = cmp_mac_address_start(packet.eth.src,starts)
    dst = cmp_mac_address_start(packet.eth.dst,starts)
    if 'ETH Layer' in str(packet.layers) and ('IP' in packet or 'IPv6' in packet) and (src or dst):
        row = make_dict(packet)
        if row is None:
            pass
#        print(row)
        source = row['src_addr']
        destination = row['dst_addr']
        if src:
            IoT_to_Internet(source, destination)
        if dst:
            Internet_to_IoT(source, destination)
	
        csv_create(row)
        connection = sqlite3.connect('/home/indiana/TtTAnakin/TtTHackTUES9/Web/TtTsite/db.sqlite3')
        sql_select_Query = "select main_iotdevice.ip from main_iotdevice"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        devices_ip=cursor.fetchall()
#       	print(devices_ip)
        for i in devices_ip:
            sql_select_Query = "select count(main_blacklist.id) from main_blacklist left join main_iotdevice on main_iotdevice.id==main_blacklist.device_id and main_iotdevice.ip==?"
            cursor = connection.cursor()
#            print("i:" + str(i))
            cursor.execute(sql_select_Query, (str(i),))
            count = cursor.fetchone()
            print(count)
            if(count == 0):
               if(blocked == True):
                    if src:
                        unblock_ip(source)
                    if dst:
                        unblock_ip(destination)
                    blocked = False
            else:
                if(blocked == False):
                    if src:
                        command = "iptables -C drop_blocked_lan_ip -i wlan0 -s 192.128.5.108 -j DROP"
                        p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                        output, err = p.communicate()
                        res = output.decode('utf-8')
                        try:
                           if res[0]:
                                print("Rule exsists")
                        except:
                           block_ip(source)
                           blocked = True
                           print("No rule")
#                    if dst:
#                       block_ip(destination)
                    blocked = True
#            connection.close()
############################
