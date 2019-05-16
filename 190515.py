""" Google Vision API Tutorial with a Raspberry Pi and Raspberry Pi 
Camera.  See more about it here: 
https://www.dexterindustries.com/howto/use-google-cloud-vision-on-the-raspberry-pi/

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
# -*- coding: utf-8 -*-
# performs a simple device inquiry, followed by a remote name request of each
# discovered device

import os
import sys
import struct
import bluetooth._bluetooth as bluez

def printpacket(pkt):
    for c in pkt:
        sys.stdout.write("%02x " % struct.unpack("B",c)[0])
    print 


def read_inquiry_mode(sock):
    """returns the current mode, or -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # read_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # first read the current inquiry mode.
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_READ_INQUIRY_MODE )

    pkt = sock.recv(255)

    status,mode = struct.unpack("xxxxxxBB", pkt)
    if status != 0: mode = -1

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    return mode

def write_inquiry_mode(sock, mode):
    """returns 0 on success, -1 on failure"""
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # Setup socket filter to receive only events related to the
    # write_inquiry_mode command
    flt = bluez.hci_filter_new()
    opcode = bluez.cmd_opcode_pack(bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    bluez.hci_filter_set_event(flt, bluez.EVT_CMD_COMPLETE);
    bluez.hci_filter_set_opcode(flt, opcode)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    # send the command!
    bluez.hci_send_cmd(sock, bluez.OGF_HOST_CTL, 
            bluez.OCF_WRITE_INQUIRY_MODE, struct.pack("B", mode) )

    pkt = sock.recv(255)

    status = struct.unpack("xxxxxxB", pkt)[0]

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )
    if status != 0: return -1
    return 0

def device_inquiry_with_with_rssi(sock):
    # save current filter
    old_filter = sock.getsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, 14)

    # perform a device inquiry on bluetooth device #0
    # The inquiry should last 8 * 1.28 = 10.24 seconds
    # before the inquiry is performed, bluez should flush its cache of
    # previously discovered devices
    flt = bluez.hci_filter_new()
    bluez.hci_filter_all_events(flt)
    bluez.hci_filter_set_ptype(flt, bluez.HCI_EVENT_PKT)
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, flt )

    duration = 4
    max_responses = 255
    cmd_pkt = struct.pack("BBBBB", 0x33, 0x8b, 0x9e, duration, max_responses)
    bluez.hci_send_cmd(sock, bluez.OGF_LINK_CTL, bluez.OCF_INQUIRY, cmd_pkt)

    results = []

    done = False
    while not done:
        pkt = sock.recv(255)
        ptype, event, plen = struct.unpack("BBB", pkt[:3])
        if event == bluez.EVT_INQUIRY_RESULT_WITH_RSSI:
            pkt = pkt[3:]
            print("test", pkt, type(pkt[0]))
            nrsp = struct.unpack(b"B", bytes(pkt[0]))[0]
            print(nrsp, type(nrsp))
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                rssi = struct.unpack("b", pkt[1+13*nrsp+i])[0]
                print("addr", addr, type(addr))
                results.append( ( addr, rssi ) )
                print ("[%s] RSSI: [%d]" % (addr, rssi))
        elif event == bluez.EVT_INQUIRY_COMPLETE:
            done = True
        elif event == bluez.EVT_CMD_STATUS:
            status, ncmd, opcode = struct.unpack("BBH", pkt[3:7])
            if status != 0:
                print ("uh oh...")
                printpacket(pkt[3:7])
                done = True
        elif event == bluez.EVT_INQUIRY_RESULT:
            pkt = pkt[3:]
            nrsp = struct.unpack("B", pkt[0])[0]
            for i in range(nrsp):
                addr = bluez.ba2str( pkt[1+6*i:1+6*i+6] )
                results.append( ( addr, -1 ) )
                print ("[%s] (no RRSI)" % addr)
        else:
            print ("unrecognized packet type 0x%02x" % ptype)
        print ("event ", event)

    # restore old filter
    sock.setsockopt( bluez.SOL_HCI, bluez.HCI_FILTER, old_filter )

    return results
def beacon():
	dev_id = 0
	try:
		sock = bluez.hci_open_dev(dev_id)
	except:
		print ("error accessing bluetooth device...")
		sys.exit(1)

	try:
		mode = read_inquiry_mode(sock)
	except:
		print ("error reading inquiry mode.  ")
		print ("Are you sure this a bluetooth 1.2 device?")
		#print e
		sys.exit(1)
	print ("current inquiry mode is %d" % mode)

	if mode != 1:
		print ("writing inquiry mode...")
		try:
			result = write_inquiry_mode(sock, 1)
		except:
		#except Exception, e:
			print ("error writing inquiry mode.  Are you sure you're root?")
			#print e
			sys.exit(1)
		if result != 0:
			print ("error while setting inquiry mode")
		print ("result: %d" % result)

	device_inquiry_with_with_rssi(sock)


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
    beacon()

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
