#!/usr/bin/python3


import numpy as np
import time
import sys, serial
 
# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)

# parse args
args = parser.parse_args()
strPort = args.port
ser = serial.Serial(strPort, 115200)  


# main() function
def main():

    received = ser.readline().decode('utf-8').strip('\x00')
    
    start = time.time()
    

    
    
    with open("test.csv", "a") as myfile:
      myfile.write(received)
      
    
    
    line = received.split('\n')[0]
    
    print("Line = "+line)
    
    y,x = line.split(',')
    
    
    
    
    xar.append(int(x))
    yar.append(int(y))
 
 # call main
if __name__ == '__main__':
  main()
