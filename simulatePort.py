#!/usr/bin/python3


import sys, serial, argparse
import numpy as np
import time
from random import randint


# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)

# parse args
args = parser.parse_args()
strPort = args.port
ser = serial.Serial(strPort, 115200) 
i=1
while(1):
  '''input_str = sys.stdin.readline().encode('utf-8')
  ser.write(input_str)
  print(input_str)'''
  reading = str(randint(1,100))+","+str(i)+"\n"
  print(str(reading).encode('utf-8'))
  ser.write(str(reading).encode('utf-8'));
  i+=1
  time.sleep(1)
  
