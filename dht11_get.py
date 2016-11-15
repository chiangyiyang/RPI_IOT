#!/usr/bin/python

import sys
import urllib2
import RPi.GPIO as GPIO
from time import sleep
from random import randint as ri
import Adafruit_DHT
import json
#import math

READ_API_KRY = "XIJWWMVIG7IBQE8H"
CHANNEL_ID = "178333"

# main() function 
def main():
  f = open('db_file', 'w+')
  while True:
    try:
      conn = urllib2.urlopen( "http://api.thingspeak.com/channels/%s/feed.json?api_key=%s" 
                           % (CHANNEL_ID, READ_API_KRY))
      response = conn.read()
      print "http status code= %s" % (conn.getcode())
      data = json.loads(response)
      #print data
      for idx, feed in enumerate(data['feeds']):
        print str(idx) + "      DH: " + feed['field1'] + ", T: " + feed['field2']
      print "End of Record"
      f.write(str(data))
      
      conn.close()
      sleep(10)
    except:
      f.close()
      print "\nExiting"
      break

#call main
if __name__ == '__main__':
  main()
