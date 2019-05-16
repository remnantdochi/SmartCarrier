import serial

from bluetooth import *
    
def main():
    ser = serial.Serial('/dev/ttyACM0',9600)
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
            if data == 'g':
                #client_sock.send(data)
                ser.write('g'.encode())
            if data == 's':
                ser.write('s'.encode())
            #print ("send [%s]" % tempchar)
    except IOError:
        pass

    print ("disconnected")

    client_sock.close()
    server_sock.close()
    print ("all done")
if __name__ == '__main__':

    main()
