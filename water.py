#Bernard Smith
#water.py
#Provides the functions to send the signal to water the plant, 
# get the status, and provide when the system was last watered

import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) #Provides pin numbering scheme
GPIO.setwarnings(False)  #Disable warning in case of different configurations


def lastWatered():
  try:
    f = open("lastWatered.txt", "r")
    return f.readline()
  except:
    return "The plant was never watered!"


def getStatus(pin = 8):
  GPIO.setup(pin, GPIO.IN) #Set pin 8 to input
  return GPIO.input(pin)


def output(pin):
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  GPIO.output(pin, GPIO.HIGH)


def autoWater(delay = 5, pumpPin = 7, waterSensorPin = 8):
  consecWater = 0
  output(pumpPin)
  print("Beginning automatic watering! Use CTRL + C to end.")
  try:
    while 1 and consecWater < 10:
      time.sleep(delay)
      moisture = getStatus(pin = waterSensorPin) == 0  #Gets moisture level from the sensor
      if not moisture:  #If sensor doesn't pick up moisture
        if consecWater < 5:
          pumpOn(pumpPin, 1)
        consecWater += 1
      else:
        consecWater = 0
  except KeyboardInterrupt: # Check for CTRL + C to exit
    GPIO.cleanup() #Cleanup after GPIO

def pumpOn(pumpPin = 7, delay = 2):
  output(pumpPin)
  f = open("lastWatered.txt", "w")
  f.write("Plant last watered {}".format(datetime.datetime.now()))
  f.close()
  GPIO.output(pumpPin, GPIO.LOW)
  time.sleep(1)
  GPIO.output(pumpPin, GPIO.HIGH)
