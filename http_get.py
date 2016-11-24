#!/usr/bin/python

import sys
import urllib2
import RPi.GPIO as GPIO
from time import sleep
from random import randint as ri
import Adafruit_DHT
import spidev
import smbus

# Define some constants from the datasheet
DEVICE = 0x23  # Default device I2C address

POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

# Start measurement at 1 lx resolution. Time typically 120ms.
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5 lx resolution. Time typically 120ms.
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 4 lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13

# Start measurement at 1 lx resolution. Time typically 120ms.
# Device is automatically set to Power Down after measurement
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5 lx resolution. Time typically 120ms.
# Device is automatically set to Power Down after measurement
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 4 lx resolution. Time typically 16ms.
# Device is automatically set to Power Down after measurement
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)

spi = spidev.SpiDev()
spi.open(0, 0)

PIR_PIN = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIR_PIN, GPIO.IN)



def converToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number
    return ((data[1] + (256 * data[0])) / 1.2)


def readLight(addr=DEVICE):
    data = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return converToNumber(data)


def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        print "wrong port num"
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcount = ((r[1] & 3) << 8) + r[2]
    return adcount


def getSensorData():
    RH, T = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 23)
    # return dict
    return (str(RH), str(T))


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
            
            gas = int(round(readadc(3) / 1.024))  # MQ2 in port:3
            print "gas:", gas
            
            light = "%.1f" % (readLight())
            print "Light Level : " + light + " lx"
            
            pir = str(GPIO.input(PIR_PIN))
            print "PIR: " + pir
            
            f = urllib2.urlopen(baseUrl +
                                "&field1=%s&field2=%s&field3=%s&field5=%s&field6=%s" % (RH, T, gas, light, pir))
            print "HTTP Response: " + f.read()
            f.close()
            sleep(20)
        except:
            print "\nExiting"
            break


# call main
if __name__ == '__main__':
    main()
