#!/usr/bin/python3


import base64
 

 
with open("opencv.png", "rb") as imageFile:
    temp = "temp"
    img = base64.b64encode(imageFile.read())
    #print(str)
    f = open('image.txt','wb')
    #f.write(str)
    i=0
    while(i<len(img)):
      temp = img[i:i+10000]
      f.write((temp+b"\n"))
      #f.write('\n')
      i=i+10000
    
    
imgdata = base64.b64decode(img)
filename = 'some_image.png'  
with open(filename, 'wb') as f:
    f.write(imgdata)
