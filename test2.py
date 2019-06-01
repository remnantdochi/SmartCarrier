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

def SmartCar_GO():
    if prev_data ==  "g":
        return
    
    print("GO")
    prev_data ="g"



def main():
    #ser = serial.Serial('/dev/ttyACM0',9600)
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    #global camera
    #camera = picamera.PiCamera()
    #command = "g"

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
    command =""
    cnt = 0
    loglist = []
    data =""
    prev_data=""
    while True:
        
        data = client_sock.recv(512)
        data = data.decode()
        

        
        
        if data == None :
            
            print("aaaaa")
        
            
                
        
        '''
        if 'l' in data:
            #client_sock.send(data)
            ser.writelines('l')
            time.sleep(0.001)
            ser.writelines('s')
            data = 'none'
            #print('left')
            continue
                
        if 'r' in data:
            ser.writelines('r')
            time.sleep(0.001)
            ser.writelines('s')
            data = 'none'
            #print('right')
            continue
        '''
        
        '''
        if data == "g":
            command = "g"
            while data=="g":
                service = BeaconService("hci0")
                devices = service.scan(1)
                
                for address, data in list(devices.items()):
                    b = Beacon(data, address)
                    
                if len(loglist) < 3 :
                    loglist.append(b._rssi)
                    cnt +=1
                else:
                    loglist[cnt%3] = b._rssi
                    cnt += 1
                x = sum(loglist)/3
                
                RSSI = 0.9*x + 0.1*b._rssi
                calculate = RSSI

                if RSSI < -80 and command == "g":
                    command = "g"
                    ser.writelines('g')
                    if b._rssi > -75:
                        command = "s"
                        
                else:
                    command ="s"
                
                ser.writelines(command)
                
                data = client_sock.recv(512)
                data = data.decode()
        
            print('exit')
            '''

                
                
                
            
            
            
        
        
        

    print ("disconnected")

    client_sock.close()
    server_sock.close()
    print ("all done")
if __name__ == '__main__':

    main()
