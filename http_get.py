#!/usr/bin/python

import sys
import urllib2
import RPi.GPIO as GPIO
from time import sleep
from random import randint as ri
import Adafruit_DHT

def getSensorData():
  RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
  # return dict
  return (str(RH),str(T))

# main() function
def main():
  # use sys.argv if needed
  if len(sys.argv) < 2:
    print('Usage: python http_get.py PRIVATE_KEY')
    exit(0)
  
  print 'starting...'
  baseUrl = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]
  
  while True:
    try:
      RH, T = getSensorData()
      print RH
      print T
      f = urllib2.urlopen(baseUrl + 
                          "&field1=%s&field2=%s" % (RH, T))
      print f.read()
      f.close()
      sleep(30)
    except:
      print "\nExiting"
      break

#call main
if __name__ == '__main__':
  main()
