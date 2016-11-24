#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 讀取HC SR501 的數值 
import RPi.GPIO as GPIO
import time

pirPin = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pirPin, GPIO.IN)

while True:
    print (GPIO.input(pirPin))
    time.sleep(0.5)





