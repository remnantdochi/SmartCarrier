#ython2 

import serial
import time
while True:
    #ser1 = serial.Serial('/dev/ttyACM_P1',9600)
    #ser2 = serial.Serial('/dev/ttyACM_RFX',9600)
    command = raw_input("command \n")
    print (command)

    try:
		ser1 = serial.Serial('/dev/ttyACM_P1',9600) 
		ser1.writelines(command)

    except:
		print("ERROR")

    try:
		ser2 = serial.Serial('/dev/ttyACM_RFX',9600) 
		ser2.writelines(command)
    except:
		print("ERROR")

