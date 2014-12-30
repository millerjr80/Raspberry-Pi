#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

# tell the GPIO module that we want to use the
# chip's pin numbering scheme

GPIO.setmode(GPIO.BCM)

# setup pins 17 and 23 as an output. Set pin 22 as an input.
GPIO.setup(22,GPIO.IN)
GPIO.cleanup()
input = GPIO.input(22)

while True:
  if (GPIO.input(22)):
    print("Button Pressed")
