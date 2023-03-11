import subprocess
import os


command = "iptables -C drop_blocked_lan_ip -i wlan0 -s 192.168.5.108 -j DROP"
p = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
(output, err) = p.communicate()
res = output.decode('utf-8')
print(res)
