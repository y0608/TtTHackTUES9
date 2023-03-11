# Project for HackTUES 9
<img src="https://user-images.githubusercontent.com/54147006/223833805-b6605af7-7064-48b1-a1cc-a11ebe7d86f6.png" alt="drawing" style="width:900px;"/>

Нашият проект цели да създаде защитна система за всички IoT устройства в нашия дом, офис и други. <br>
Presentation: https://prezi.com/view/wxg1Yyg6mbjlCkAzTpi7/
<br/>

# TtT IoT Firewall - Firewall for all of your IoT devices


## Тема: 
<img src="https://user-images.githubusercontent.com/54147006/224448143-e8f24e65-76ab-4857-937e-cd4f2e2be7ae.png" alt="drawing" style="width:400px;"/>

🟣 IoT & smart home security



## Проблемът
Според проучване на фирмата за сигурност Extreme Networks почти **70%** от организациите са претърпели **атаки** срещу своите IoT устройства. И много от тези атаки са **довели до пробив**. Този зашеметяващ брой ясно показва защо мрежовата сигурност на IoT е толкова важен аспект за поддържане на сигурността. 

Ботнетът Mirai, който през 2017 г. отприщва distributed denial-of-service (**DDoS**) срещу големи уебсайтове с помощта на милиони **компрометирани IoT устройства**.

Нашият проект решава точно този проблем, като прекарва интернет трафика на IoT устройствата през Raspberry pi и това позволява да спираме нежелан трафик.


## Функционалност

#### Raspberry pi
Конфигурираме нашия Raspberry pi да работи като **AccessPoint** към рутер свързан с интернет.

Насочваме **целия трафик** на IoT устройствата, като ги свързваме с Raspberry pi-я. Той може да бъде заместен с всеки unix базирано устройство.

Така ние създаваме още една защитна стена, която проверява дали трафикът е **зловреден**:
това става като *допускаме*, че в началото първите няколко адреса са Cloud provider-ите на IoT устройствотo.

<img src="https://user-images.githubusercontent.com/54147006/224466525-6257799c-ea5f-4923-a91f-05da1c92cab5.png" alt="drawing" style="width:700px;"/>

#### Комуникация
При комуникация **IoT -> Internet** - наблюдаваме дали IoT устройството изпраща към Cloud Provider, който е позволен. Ако не то това е недопустимо поведение и се блокира.<br>
При комуникация **Internet -> IoT** - ще наблюдаваме дали трафикът наподобява предишен трафик и ще решим дали да го блокираме или не.*(все още не е реализирано)*


В демото използваме 4G modem и блок схемата изглежда така:
<img src="https://user-images.githubusercontent.com/54147006/224460359-d85db717-a031-462c-afcc-f1c13b4665e5.png" alt="drawing" style="width:700px;"/>


#### Web application
Чрез web application на локалната мрежа се управляват усторйствата и блокираните адреси. През него даваме команда за намиране на IoT устройствата в нашата **локална мрежа**. През приложението може да **управляваме трафика на IoT устройствата** и blacklist и whitelist адресите на всеки един от тях.

За да бъдат локализирани Iot устройствата в мрежата, е достатачно да се натисне бутон, който извиква IoT finder. 

#### IoT finder
Когато програмата **iot_devices_finder.py** се задейства и мак адресите и ip адресите на всички нови iot устройства се записват. Ние разбираме mac адресите на IoT устройствата, като **наблюдаваме трафика**, когото те изпращат.

Трафикът в една мрежа **няма** да бъде само от устройства, чийто трафик ние искаме да следим. Затова преди да добавим някой мак адрес проверяваме дали **началото му**(Organizationally Unique Identifier (OUI)) **съотвества** на някое от iot_devices_mac_addresses.txt. В този файл са **предварително записани** началата на мак адреси на iot устройства.

## В бъдеще
<ul>
 <li>В бъдеще ще направим изкуствения интелект, който определя дали един трафик е зловреден или не. Това може да се направи с повече данни от трафик.
 <li>Ще обработваме IPv6. В момента не го правим, защото в момента нашият модем няма IPv6 адрес и съответно не може да комуникира чрез него
 <li>Повече функционалности в web appa
 <li>Facial recognition при логването в приложението на локалната мрежа
</ul>

## Технологии
- Python - Wireshark, Django
- Raspberry pi
- ESP32

## Части(ако има хардуер)
- Raspberry pi - firewall/access point 
- ESP32 - симулира смарт устройствата
- 4g modem - за симулацията

## Инсталация - как се инсталира проекта

Свързвате Rpi-я към рутера, пускаме го, отваряме web application на локалната мрежа и пускаме да се търсят устройства.

#### 
	sudo apt install wireshark
	sudo apt install tshark

##### Python библиотеки
```import pyshark
import datetime
import sqlite3
import csv
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import telebot
import subprocess
import sys
```
##### библиотеки за ESP-то, като симулация:
``` 
https://github.com/marian-craciunescu/ESP32Ping
```

### Отбор
 - Живко(капитан)
 - Митко
 - Виктор
 - Йоан
 - Ради

### Версии
- v1 - in development
