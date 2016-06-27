#!/usr/bin/python3

import os
import serial 
import json
import sys
import struct
import argparse
import time

import zmq
from  multiprocessing import Process


# create parser
parser = argparse.ArgumentParser(description="Serial")
# add expected arguments
parser.add_argument('--port', dest='port', required=True)
parser.add_argument('--baud', dest='baud', required=True)
# parse args
args = parser.parse_args()
strPort = args.port
strbaud = args.baud
try:
  comm = serial.Serial(strPort, strbaud, timeout=0, xonxoff=False, rtscts=False, dsrdtr=False)
except:
  print("Bad port")
  sys.exit()
print ("baud = "+strbaud+"\nport = "+strPort+"\nStarted Receiving")
line = ""


class storage:
  def __init__(self):
      
    # Initialize a zeromq context
    self.context = zmq.Context()
 
    # Set up a channel to send work
    self.ventilator_send = self.context.socket(zmq.REP)
    self.ventilator_send.connect('tcp://127.0.0.1:5588')
    
    if not os.path.exists("test.csv"):
      with open("final.csv", "a") as myfile:
        myfile.write("<TEAM_ID>,<MISSION_TIME>,<PACKET_COUNT>,<ALT_SENSOR>,<PRESSURE>,<SPEED>,<IN_TEMP>,<VOLTAGE>,<GPS_LATITUDE>,<GPS_LAT_CHAR>,<GPS_LONGITUDE>,<GPS_LON_CHAR>,<GPS_ALTITUDE>,<GPS_SAT_NUM>,<GPS_SPEED>,<LAST_COMMAND_TIME>,<COMMAND_COUNT>,<FSW STATE>,<OUT_TEMP>\n")
        

  def main(self):
    lastPacketCount = 0
    flag=0
    while(1):
      try:
        global line
        received=""
        nflag=1
        nnflag=0
        contf = 0
        while 1:
          receive = comm.readline().decode('utf-8').strip('\x00')
          if(receive==""):
            continue
          with open("cansat16.log", "a") as logfile:
           logfile.write(receive+'\n......................')

          if(contf == 1):
            received = contl
            contf = 0
            nnflag = 1
          if (nnflag==0 and "S" in receive):
            received = received + receive.split('S')[nflag]
            nnflag=1
            if(nflag == 1):
                nflag=0
                continue
          if(nnflag==1 and "S" not in receive):
            received = received + receive
            continue
          if(nnflag ==1 and "S" in receive):
            received = received + receive.split('S')[0]  
            if("SS" in receive):
                contf = 1
                contl = receive.split('SS')[1]
            break
          

        readings = received.split(',')

        if(received==""): 
          continue
        if(len(readings)!=19):
            continue
        
        if(readings[2]==lastPacketCount):
            continue
        lastPacketCount = readings[2]
        #TODO acknowledge
        #comm.write(("Received"+str(readings[1])).encode('utf-8'));
       
        line = ""
        
        readings[14] = str(float(readings[14]) * 0.5144)
        readings[5] = str(float(readings[5]) * 0.00508)
        readings[0] = "1001"
        
        
        
        
        for i in range(19):
            if(i==0):
                line = readings[i]    
            else:
                line = line + "," + readings[i]

        
        
        with open("final.csv", "a") as myfile:
          myfile.write(line+'\n')
        jsonReadings = {}
        jsonReadings["TeamID"] = readings[0]
        jsonReadings["MissionTime"] = readings[1]
        jsonReadings["PacketCount"] = readings[2]
        jsonReadings["AltSensor"] = readings[3]
        jsonReadings["Pressure"] = readings[4]
        jsonReadings["Speed"] = readings[5]
        jsonReadings["InTemp"] = readings[6]
        jsonReadings["Voltage"] = readings[7]
        jsonReadings["GPSLatitude"] = readings[8]
        jsonReadings["GPSLatChar"] = readings[9]
        jsonReadings["GPSLongitude"] = readings[10]
        jsonReadings["GPSLonChar"] = readings[11]
        jsonReadings["GPSAltitude"] = readings[12]
        jsonReadings["GPSSatNum"] = readings[13]
        jsonReadings["GPSSpeed"] = readings[14]
        jsonReadings["LastCommandTime"] = readings[15]
        jsonReadings["CommandCount"] = readings[16]
        jsonReadings["State"] = readings[17]
        jsonReadings["OutTemp"] = readings[18]
        print("done")
        
        json_data = json.dumps(jsonReadings)
       
        msg = self.ventilator_send.recv()
        self.ventilator_send.send(json_data.encode("utf-8"))
        
        if(msg==b'c'):
            self.takeImage()
                    
        
      except:
        pass
        
        
  def takeImage(self):
    print("Image command sent!")
    comm.write(struct.pack('>H',99))
    
  def triggerFailsafe(self):
    #TODO failsafe
    print("Triggered")
  def disconnectTelemetry(self):
    #TODO disconnect
    print("Disconnected")
  def reconnectTelemetry(self):
    #TODO reconnect
    print("Reconnected")
    

if __name__=="__main__":
  store = storage()
  store.main()
