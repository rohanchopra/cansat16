#!/usr/bin/python3


import sys, serial, argparse
import numpy as np
import time


# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)

# parse args
args = parser.parse_args()
strPort = args.port
ser = serial.Serial(strPort, 115200) 
print(ser)
while(1):
  ser.write(sys.stdin.readline().encode('utf-8'))
