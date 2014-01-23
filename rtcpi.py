#!/usr/bin/env python3
#read MCP3424 adc chips

import quick2wire.i2c as i2c

import time
import sys, math, struct

rtc_address1 = 0x68
with i2c.I2CMaster(1) as bus:
	
#bus.transaction(i2c.writing_bytes(adc_address1, 0X00, 0X0C))

	def GetTime():
		
		#bus.transaction(
		#i2c.writing_bytes(rtc_address1, 0xFE, 0x2C))
		time.sleep(0.05)
		seconds, minutes, hours, dayofweek, day, month, year = bus.transaction(
			i2c.writing_bytes(rtc_address1, 0),
			i2c.reading(rtc_address1,7))[0]
		
		print ("%02d - %02d - %02d- %02d:%02d:%02d " % (fromBCDtoDecimal(year), 
			fromBCDtoDecimal(month), fromBCDtoDecimal(day)
			,fromBCDtoDecimal(hours), fromBCDtoDecimal(minutes), 
			fromBCDtoDecimal(seconds & 0x7F)))
		
		
	def fromBCDtoDecimal(x):
		return x - 6 * (x >> 4)
		#return (newvalue /16 * 10) + (newvalue%16)
		
	def bin2bcd(x):
		return x + 6 * (x /10)
	
	bus.transaction(i2c.writing_bytes(rtc_address1, 0x00, 0x0C, 0x0C, 
		0x0C,  0x00, 0x0C, 0x0C, 0x0C, 0x00))	
			
	while True:
		GetTime()
