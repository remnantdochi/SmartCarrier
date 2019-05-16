import serial
import time
ser = serial.Serial('/dev/ttyACM0',9600)
while True:
	command = raw_input("read \n")
	print (command)
	ser.writelines(command)
