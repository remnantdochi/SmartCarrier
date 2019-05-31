#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from gattlib import BeaconService
import serial
import time
import math
#ser = serial.Serial('/dev/ttyACM0',9600)
command =""

class Beacon(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR}"\
                " minor:{MINOR} txpower:{POWER} rssi:{RSSI}"\
                .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
                        MINOR=self._minor, POWER=self._power, RSSI=self._rssi)
        return ret

#service = BeaconService("hci0")
#devices = service.scan(2)
loglist=[]
cnt = 0
RSSI =0
w=0.9
while True:
        
        service = BeaconService("hci0")
        devices = service.scan(1)
        print(service, devices)
        
        for address, data in list(devices.items()):
            #b = Beacon(data, address)
            b = Beacon(data, address)
            #l = math.log(abs(b._rssi))
            #print(b._address, b._rssi)

        #print("Done.")
        print(b._address, b._rssi)
        
        #command = raw_input("command \n")
        if len(loglist) < 3 :
            loglist.append(b._rssi)
            cnt +=1
        else:
            loglist[cnt%3] = b._rssi
            cnt += 1
        

        x = sum(loglist)/3
        
        RSSI = w*x + (1-w)*b._rssi
        print(RSSI)
        
        command = "g"
        
        if RSSI < -80 and command == "g":
            command = "g"
            if b._rssi > -75:
                command = "s"
        else:
            command ="s"
        
        print(command)

        
        #ser.writelines(command)
        time.sleep(0.5)

                
        #print (command)
        #ser.writelines(command)
        
