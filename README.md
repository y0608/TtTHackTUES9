# Project for HackTUES 9
<img src="https://user-images.githubusercontent.com/54147006/223833805-b6605af7-7064-48b1-a1cc-a11ebe7d86f6.png" alt="drawing" style="width:800px;"/>

Нашият проект цели да създаде защитна система за всички IoT устройства в нашия дом, офис или друго.

gif demo?

<br/>

# TtT pager - Space communication system
## Content table?

## Тема:
снимка на темата от дискорд 


🟣 подтема

<br/>

## Функционалност
Основната функционалност на проекта <br/><br/>

Конфигурираме Rpi да работи като AccessPoint към рутер свързан с интернет. Свързваме IoT устройствата с AP-а като по този начин пренасочваме трафика към и от IoT устройствата да минава винаги през Rpi-я. Така ние създаваме още една защитна стена, която проверява дали трафикът е зловреден. Това става като допускаме в началото първите няколко адреса, които разчитаме, че са Cloud provider-ите на IoT устройството. 
При комуникация IoT - Internet - наблюдаваме дали IoT устройството изпраща към Cloud Provider, ако не то това е недопостимо поведение и се блокира ip адреса на IoT устройството.
При комуникация Internet - IoT - наблюдаваме дали трафикът наподобява на предишен трафик и решаваме дали да го блокираме или не.

Има web application на локалната мрежа през, който се управляват блокираните адреси. Там има бутон, чрез който намираме IoT устройствата в нашата локална мрежа, за да е по сигурно.

## Архитектура
#### - Frontend

#### - Backend

#### - Комуникация

#### - ...

### В бъдеще
 
 В бъдеще трябва да се подобри изкуственият интелект, който определя дали един трафик е зловреден или не. Това може да се направи с повече данни от трафик. 

### Технологии
-

Python, Rpi, ESP32, ML, Telegram, Linux

### Части(ако има хардуер)
- 
- ESP32, Rpi, modem - за симулация

### Инсталация - как се инсталира проекта

Свързвате Rpi-я към рутера, пискаме го, отваряме web application на локалната мрежа и пускаме да се търсят устройства

#### 
	Wireshark и Tshark трябва да се изтеглят със sudo

##### Python библиотеки
```import pyshark
import datetime
import sqlite3
import csv
import os
import pyshark
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import telebot
```
##### библиотеки за ESP-то, като симулация:
``` https://github.com/marian-craciunescu/ESP32Ping
```

### Отбор
 - Живко(капитан)
 - Митко
 - Виктор
 - Йоан
 - Ради

### Версии
- v1 - in development
