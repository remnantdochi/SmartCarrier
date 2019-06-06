"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/
Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.
This script uses the Vision API's label detection capabilities to find a label
based on an image's content.
"""

import serial

from bluetooth import *

from gattlib import BeaconService
import serial
import time
import math

import picamera

from google.cloud import vision

client = vision.ImageAnnotatorClient()

from bluetooth import *

from gattlib import BeaconService
import serial
import time
import math

ser = serial.Serial('/dev/ttyACM0', 9600)
command = ""


def takephoto():
    print("takephoto")
    camera.capture('cam.jpg')


def machine():
    takephoto()  # First take a picture
    """Run a label request on a single image"""

    with open('cam.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    tempchar = []
    for i in range(min(3, len(labels))):
        print(labels[i].description)
        tempchar.append(labels[i].description)
    finaldata = ','.join(tempchar)
    return finaldata


class Beacon(object):

    def __init__(self, data, address):
        self._uuid = data[0]
        self._major = data[1]
        self._minor = data[2]
        self._power = data[3]
        self._rssi = data[4]
        self._address = address

    def __str__(self):
        ret = "Beacon: address:{ADDR} uuid:{UUID} major:{MAJOR}" \
              " minor:{MINOR} txpower:{POWER} rssi:{RSSI}" \
            .format(ADDR=self._address, UUID=self._uuid, MAJOR=self._major,
                    MINOR=self._minor, POWER=self._power, RSSI=self._rssi)
        return ret


def main():
    server_sock = BluetoothSocket(RFCOMM)
    server_sock.bind(("", PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    global camera
    camera = picamera.PiCamera()

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service(server_sock, "AquaPiServer",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE],
                      #                   protocols = [ OBEX_UUID ]
                      )

    print("Waiting for connection on RFCOMM channel %d" % port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from ", client_info)

    command = ""
    cnt = 0
    loglist = []
    data = ""
    flag = 0

    prev_data = ""

    while True:

        try:
            data = client_sock.recv(1024)
            data = data.decode()
            print(data, "AAAAAAAAA")

        except:
            ser.flushInput()
            read_serial = ser.readline()
            uu_dist = read_serial[:-2]
            try:
                u_dist = float(uu_dist)
            except:
                u_dist = 800.0

            if flag == 0:
                print("time out")
                continue

        # print(data, type(data))

        if flag == 0:
            flag = 1
        if data == "cam":
            client_sock.setblocking(2)
            # client_sock.settimeout(0)
            print('running')
            prev_data = "cam"

            data_machine = machine()
            myfile = open('cam.jpg', 'rb')
            sbytes = myfile.read()
            file_size = str(len(sbytes))
            client_sock.send(file_size)
            client_sock.sendall(sbytes)
            # client_sock.send(b'end')
            client_sock.send(data_machine)

        # print("data:", data)
        print(data, "BBBBBBBBB")

        if data == "start":
            prev_data = "start"
            client_sock.setblocking(0)
            client_sock.settimeout(0.1)

            if (flag == 0 or flag == 1):
                ser.flushInput()
                read_serial = ser.readline()
                uu_dist = read_serial[:-2]
                try:
                    u_dist = float(uu_dist)
                except:
                    u_dist = 800.0
                flag = 2
                command = "g"
                ser.writelines('g')

            service = BeaconService("hci0")

            try:
                for i in range(10):
                    devices = service.scan(2)
                    if devices != {}:
                        break
                prev_devices = devices


            except:
                devices = prev_devices

            for address, beacon_data in list(devices.items()):
                b = Beacon(beacon_data, address)

            print("prev : ", command)

            if command == "g":
                if u_dist < 600:
                    command = "s"
                    ser.writelines('s')
            else:
                if b._rssi < -75 and u_dist >= 600:
                    command = "g"
                    ser.writelines('g')

            print(b._rssi, u_dist, command)





        elif data == "l" and prev_data == "start":
            print('left')
            data = "start"
            ser.writelines('l')
        elif data == "r" and prev_data == "start":
            print('right')
            ser.writelines('r')
            data = "start"
        elif data == "end":
            print('end')
            flag = 0
            ser.writelines('s')
            break
        else:
            data = "start"

    print("disconnected")

    client_sock.close()
    server_sock.close()
    print("all done")


if __name__ == '__main__':
    main()
