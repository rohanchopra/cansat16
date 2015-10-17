#!/usr/bin/python3


import sys, serial, argparse
import numpy as np
import time
from random import randint


#First is input
#Second is output

# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)

# parse args
args = parser.parse_args()
strPort = args.port
ser = serial.Serial(strPort, 9600)  #Open serial connection st specified port


i=1
while(1):
  
  #Simulating string received from xbee
  reading = "132,"+str(i)+","+str(randint(1,1000))+","+str(randint(1,1000))+","+str(randint(1,100))+","+str(randint(1,30))+","+str(randint(1,10))+","+str(randint(1,100))+","+str(randint(1,100))+","+str(randint(1,1000))+","+str(randint(1,6))+","+str(randint(1,100))+","+str(randint(1,100))+","+str(i)+"\n"
  
  
  print(str(reading).encode('utf-8'))
  #TODO acknowledge code
  #while(1):
  #  if(i!=1):
  #    rec = ser.readline().decode('utf-8').strip('\x00')
  #    print(rec)
  #  if(i==1 or (rec=="Received"+str(i))):
  #      ser.write(str(reading).encode('utf-8'))
  #      break
  ser.write(str(reading).encode('utf-8'))  
  i+=1
  time.sleep(1) #transmitting every 1 second
  
