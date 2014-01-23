#!/usr/bin/env python

from smbus import SMBus
import re

import time
import sys, math, struct

rtc_address1 = 0x68

# detect i2C port number and assign to i2c_bus
for line in open('/proc/cpuinfo').readlines():
    m = re.match('(.*?)\s*:\s*(.*)', line)
    if m:
        (name, value) = (m.group(1), m.group(2))
        if name == "Revision":
            if value [-4:] in ('0002', '0003'):
                i2c_bus = 0
            else:
                i2c_bus = 1
            break
               

bus = SMBus(i2c_bus)


def GetTime():
	seconds, minutes, hours, dayofweek, day, month, year = bus.read_i2c_block_data(rtc_address1, 0, 7)
	print ("%02d - %02d - %02d- %02d:%02d:%02d " % (fromBCDtoDecimal(year), 
			fromBCDtoDecimal(month), fromBCDtoDecimal(day)
			,fromBCDtoDecimal(hours), fromBCDtoDecimal(minutes), 
			fromBCDtoDecimal(seconds & 0x7F)))


def fromBCDtoDecimal(x):
	return x - 6 * (x >> 4)
		
def bin2bcd(x):
	return x + 6 * (x /10)
bus.write_byte_data(rtc_address1, 0x00, 0x00)
bus.write_byte_data(rtc_address1, 0x01, 0x0C)
bus.write_byte_data(rtc_address1, 0x02, 0x0C)
bus.write_byte_data(rtc_address1, 0x03, 0x0C)
bus.write_byte_data(rtc_address1, 0x04, 0x00)
bus.write_byte_data(rtc_address1, 0x05, 0x0C)
bus.write_byte_data(rtc_address1, 0x06, 0x0C)
bus.write_byte_data(rtc_address1, 0x07, 0x00)

			
while True:
	GetTime()
