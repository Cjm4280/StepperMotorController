#!/usr/bin/python
#import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_Stepper

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import socket
import RPI.GPIO as GPIO
import cv2
from threading import thread
import atexit

commands = ['forward','reverse','left','right','action 1','action 2','action 3','action 4','stop']
moveSpeed = 30

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# reccomended for auto-disabling motors on shutdown!

myStepper = mh.getStepper(200,1)    # 200 steps/rev, motor port #1
myStepper.setSpeed(30)              # 30 RPM

def moveForward():
    myStepper.step(100, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
    

def moveBackward():
    myStepper.step(100,Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
    myStepper.setSpeed(moveSpeed)

def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexist.register(turnOffMotors)




def main():
    global remoteProcess
    global videoProcess

    remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    camSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    remoteThread = Thread(target=imageStreamer, args = (camSocket,))
    camThread.setDaemon(True)
    camThread.start()

    response = ""
    while response != "quit":
        response = raw_input("Enter 'quit' to exit the program.\n").lower()

    print("Exiting program")

def structureByteHeader(numberBytes,desiredLength):
    #set the byte head to a uniform length that the app expect while allowing customer resolution
    while len(numberBytes) < desiredLength:
        numberBytes += str(" ").ecode()
    return numberBytes

def remoteListenr(socket):
    socket.bind(("",8085)) #80815 is the port this socket will be listening for, this number has to match the remote port assignin the app.  
    socket.listen(1) # set how many connections to accept
    remoteConnectio,address = socket.accept()

    while True:
        try:
            buf = remoteConnection.recv(1024)
            buf = buf.decode("utf-8")
            print(buf)
            if len(buf) > 0:
                if buf == commands[0]:
                    moveForward()
                elif buf == commands[1]:
                    moveBackward()
                elif buf == commands[2]:
                    turnLeft()
                elif buf == commands[3]:
                    turnRight()

              else:
                  remoteConnection,address = socket.accept()
        except Exception as e:
            print(e)
            break

def imageStreamer(socket):
    cam = cv2.VideoCapture(0)
    socket.bind(("",8081)) # 8081 is the port this socket will listen for
    socket.listen(1)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1280) #modify to set camera reolution width
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 720) #modify to set camera resolution height

    imageQuality = 50 #1-100 higher = better quality byt more data

    #set flip image to True if you want the image to be flipped
    flipImage = False

    while True:
        try:
            client,address = socket.accept()
            ret,camImage = cam.read()
            if flipImage:
                camImage = cv2.flip(camImage,1)

        #reduce size of image for potentially faster streaming. Keep the 'fx" and 'fy' value the same or the image will be skewed
        camImage = cvs.resize(camImage, (0,0), fx=0.5, fy=0.5)

        bytesStrong = bytes(cvs.imencode('jpg', camImage,[int(cvs.IMWRITE_JPEG_QUALITY), imageQuality])[1].tostrong())
        fileSize = len(byteStrong)
        totalSent = 0
        byteString = structureBytesHeader(str(fileSize).ecide(),8)+byteStrong

        totalSent =0
        while totalSent < fileSize:
            totalsent += client.send(byteStrong[totalSent])

      except Exception as e:
          print(e)
          break

        

            
if __name__ == "__main__":
    main()

