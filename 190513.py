"""
Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi Camera.  See more about it here:  https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

Use Google Cloud Vision on the Raspberry Pi to take a picture with the Raspberry Pi Camera and classify it with the Google Cloud Vision API.   First, we'll walk you through setting up the Google Cloud Platform.  Next, we will use the Raspberry Pi Camera to take a picture of an object, and then use the Raspberry Pi to upload the picture taken to Google Cloud.  We can analyze the picture and return labels (what's going on in the picture), logos (company logos that are in the picture) and faces.

This script uses the Vision API's label detection capabilities to find a label
based on an image's content.

"""

import picamera

from google.cloud import vision
client = vision.ImageAnnotatorClient()
camera = picamera.PiCamera()
# file: rfcomm-server.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a server application that uses RFCOMM sockets
#
# $Id: rfcomm-server.py 518 2007-08-10 07:20:07Z albert $

from bluetooth import *

def takephoto():
    #camera = picamera.PiCamera()
    print("takephoto")
    #client_sock.send("takephoto")
    #global camea
    camera.capture('cam.jpg')

def machine():
    takephoto() # First take a picture
    """Run a label request on a single image"""

    with open('cam.jpg', 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    tempchar=[]
    for i in range(min(3,len(labels))):
        print(labels[i].description)
        tempchar.append(labels[i].description)
    finaldata = ','.join(tempchar)
    return finaldata
    
def main():
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    #global camera
    #camera = picamera.PiCamera()

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

    try:
        while True:
            data = client_sock.recv(1024)
            client_sock.send("recieve")
            data = data.decode()
            print(data, type(data))
            if data == "cam":
                print('running')
                data = machine()
                #takephoto()
                #myfile=open('cam.jpg', 'rb')
                #sbytes=myfile.read()
                #print(type(sbytes))
                #print(len(sbytes))
                #print(sbytes)
                #client_sock.sendall(sbytes)
                #client_sock.send('end')
                client_sock.send(data)
            #print ("send [%s]" % tempchar)
    except IOError:
        pass

    print ("disconnected")

    client_sock.close()
    server_sock.close()
    print ("all done")
if __name__ == '__main__':

    main()
