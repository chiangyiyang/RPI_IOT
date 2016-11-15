#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 讀取MQ2 的數值 
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
count = 0


def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        print "wrong port num"
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcount = ((r[1] & 3) << 8) + r[2]
    return adcount


while True:
    # tmp1 = int(round(readadc(0) / 1.024))q
    # tmp2 = int(round(readadc(1) / 1.024))
    # tmp3 = int(round(readadc(2) / 1.024))
    tmp4 = int(round(readadc(3) / 1.024))  # MQ2 in port:3
    print "gas:", tmp4
    count = count + 1
    time.sleep(1)
