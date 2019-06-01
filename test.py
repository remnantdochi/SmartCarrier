import serial

from bluetooth import *

#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from gattlib import BeaconService
import serial
import time
import math


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
def main():
    ser = serial.Serial('/dev/ttyACM0',9600)
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "AquaPiServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
    print ("Waiting for connection on RFCOMM channel %d" % port)
    client_sock, client_info = server_sock.accept()
    print ("Accepted connection from ", client_info)
    client_sock.send("connect")
    client_sock.setblocking(0)
    client_sock.settimeout(0.5)
    command =""
    cnt = 0
    loglist = []
    data = ""
    flag = 0
    while True:
        try:
            data = client_sock.recv(512)
            data = data.decode()
        except:
            if flag == 0:
                print("time out")
                continue
                
        
        print(data)
        
        if flag == 0 :
            flag = 1
        
        if data == "start":
            
            print("GGGG")
            service = BeaconService("hci0")
            devices = service.scan(2)
            for address, beacon_data in list(devices.items()):
                b = Beacon(beacon_data, address)

            if len(loglist) < 3 :
                loglist.append(b._rssi)
                cnt +=1
            else:
                loglist[cnt%3] = b._rssi
                cnt += 1
            x = sum(loglist)/3
            
            RSSI = 0.9*x + 0.1*b._rssi
            #print(RSSI,'rssi')
            calculate = RSSI
            #calculate = (sum(loglist)-max(loglist)-min(loglist))/8
            #print('rssi',calculate)
            command = "g"
            if RSSI < -80 and command == "g":
                command = "g"
                #print(command)
                ser.writelines('g')
                if b._rssi > -75:
                    command = "s"
                    #print(command)
                    ser.writelines('s')
            else:
                command ="s"
                #print(command)
        elif data == "l":
            print('l')
            data = "start"
            ser.writelines('l')
        elif data == "r":
            print('r')
            ser.writelines('r')
            data = "start"
        elif data =="end":
            print('end')
            flag = 0
            client_sock.close()
            server_sock.close()
            break
        

        ## only turn when close
        
            #print('s',loglist)
        
        #ser.writelines(command)
        #print(command,loglist)
        #else : ser.writelines('g')
            #print ("send [%s]" % tempchar)

            #else :
    #except IOError:
        #pass



    #client_sock.close()
    #server_sock.close()
    print ("all done")
if __name__ == '__main__':

    main()
