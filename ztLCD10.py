#!/usr/bin/python2.7
#-*- coding: UTF-8 -*-
import commands
import os
import thread
import time
import random
import sys
import Adafruit_DHT

#from subprocess import *
from time import sleep, strftime
from datetime import datetime
from lcd2usb import LCD

#
ECHO_NUM = 100
def lcd_echo(lcd):
	errors = 0
	for _ in range(ECHO_NUM):
		val = random.randint(0, 0xffff)
		ret = lcd.echo(val)
		if val != ret:
			errors += 1
	if errors:
		print ('ERROR: %d out of %d echo transfers failed!' % (errors,ECHO_NUM))
		exit()
	else:
		print ('Echo test successful!')
			
	
USB = os.popen('lsusb')
A = USB.read()
if (A.find("lcd2usb")==-1):
	print ('NO device!')
	exit()
else:
	lcd = LCD()
	#lcd_echo(lcd)


################---变量区---##############
briLD  = 90			#亮度
conDBD = 164		#对比度
##########################################

########设置###########
lcd.set_brightness(briLD)
lcd.set_contrast(conDBD)
#######################
#lcd.clear()
exit_flag = 0

def Loading():
	lcd.home()
	lcd.clear()
	lcd.goto(1,0)
	lcd.write('LCD status display')
	sleep(0.5)
	lcd.goto(3,1)
	lcd.write('raspberry pi')
	sleep(0.5)
	lcd.goto(4,2)
	lcd.write('=Moeyuuko=')
	sleep(0.5)
	lcd.goto(5,3)
	lcd.write('[v10.0]')
	sleep(0.5)

thread.start_new_thread(Loading,())


def end_1():
	sleep(1)
	lcd.clear()
	lcd.goto(0,1)
	lcd.write("Program End =w=")
	print ('\nProgram End =w=')
	lcd.goto(0,2)
	lcd.write(datetime.now().strftime('%m/%d %w %p %l:%M:%S'))
	sleep(0.5)
	lcd.set_brightness(30)
	sleep(1)
	lcd.close()

#重启程序
def restart_program():
  python = sys.executable
  os.execl(python, python, * sys.argv)



#
def get_cpu_used():
	cpu_used = commands.getoutput( 'top -n 2 -d 0.5| grep Cpu' ).split()[24]
	return 100 - float(cpu_used)
#
def get_cpu_temp():
	tmpFile = open( '/sys/class/thermal/thermal_zone0/temp' )
	cpu_temp = tmpFile.read()
	tmpFile.close()
	return round(float(cpu_temp)/1000, 1)
#
def get_cpu_freq():
	tmpFile = open( '/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq' )
	cpu_freq = tmpFile.read()
	tmpFile.close()
	return float(cpu_freq)/1000
#
def get_gpu_temp():
	gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_temp' ).replace( 'temp=', '' ).replace( '\'C', '' )
	return float(gpu_temp)
#
def get_gpu_freq():
	gpu_temp = commands.getoutput( '/opt/vc/bin/vcgencmd measure_clock core' ).replace( 'frequency(1)=', '' )
	return float(gpu_temp)/1000000
#
def get_men_total():
	tmpFile = open( '/proc/meminfo' )
	lines = tmpFile.readlines()
	mem_total = round(float(lines[0].split()[1]) / 1024, 1)
	return mem_total
#
def get_men_used():
	tmpFile = open( '/proc/meminfo' )
	lines = tmpFile.readlines()
	#mem_total   = round(float(lines[0].split()[1]) / 1024, 1)
	mem_free    = round(float(lines[2].split()[1]) / 1024, 1)
	#men_used = mem_total - mem_free
	return mem_free
#
def get_disk_total():
	disk_used = round(float(commands.getoutput( 'df -m / | grep /' ).split()[1]) / 1024, 1)
	return disk_used
#
def get_disk_used():
	disk_used = round(float(commands.getoutput( 'df -m / | grep /' ).split()[2]) / 1024, 1)
	return disk_used
#

def get_ip_addr():
	ip_addr = commands.getoutput( 'hostname -I' )
	if ip_addr:
		return ip_addr
	else:
		return 'No network'
#
def DHT():
	global wd2
	global exit_flag
	sensor = Adafruit_DHT.DHT22
	pin = 4  #GPIO4
	while exit_flag != 1:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
    			wd2 = 'T{0:0.1f} H{1:0.1f}'.format(temperature, humidity)
		else:
			wd2 = 'Temp_Error'
		sleep(5)
#
def SSTS():
	for i in range(256)[::-1]:
		lcd.set_brightness(i)
		#time.sleep(0.001)
	for i in range(256):
		lcd.set_brightness(i)
		#time.sleep(0.001)
	lcd.set_brightness(briLD) 
#
def Network_Availability():
	global network
	global CCC
	global exit_flag

	while exit_flag != 1:
		CCC = str(get_ip_addr())
		if  CCC == 'No network':
			network = '000'
		else:
			network = '111'
		sleep(1.1)
#
def Network_speed():
	global wlsd
	global exit_flag
	while exit_flag != 1:
		A=os.popen('ifstat -i eth0  1 1')
		wlsd=A.read();
		wlsd = wlsd.replace("       eth0       \n KB/s in  KB/s out\n", " ");
		wlsd = wlsd.replace("\n", " ");
		wlsd = wlsd.replace("  ", " ",5);
		sleep(1.3)


def Key_Daemon():  #按键状态
	global layout
	global lcd
	global exit_flag
	global reload
	global errors
	
	reload_set = 8
	layout_MAX = 2
	layout_MIN = 0 

	reload = reload_set
	while exit_flag != 1:
		if errors == 0:
			key2, key1 = lcd.keys
			if key2 :
				layout = layout+1
				if layout > layout_MAX:
					layout = layout_MAX
			key2, key1 = lcd.keys
			if key1 :
				layout = layout-1
				if layout < layout_MIN:
					layout = layout_MIN
			key2, key1 = lcd.keys
			while(key1 or key2):
				key2, key1 = lcd.keys
				if layout == 0:
					if key1:
						while(key1):
							key2, key1 = lcd.keys
							if reload == 0:
								exit_flag = 1
								end_1()
								time.sleep(1)
								restart_program()
								break
							elif reload > 0:
								reload=reload-1
							time.sleep(1)
						reload = reload_set
				time.sleep(0.1)
			time.sleep(0.1)

######

def main_layout():   #主屏幕
	global wd2
	global network
	global wlsd
	global exit_flag
	A = datetime.now().strftime('%Y ')+'cpu:'+str(get_cpu_temp())+'C '+str(get_cpu_used())+'%'
	B = str(get_men_used())+'MB'

	lcd.clear()
	lcd.home()
	lcd.goto(19,2)
	lcd.write('o')
	lcd.goto(0,0)
	lcd.write(A)
	lcd.goto(0,1)
	lcd.write(B)
	lcd.goto(8,1)
	lcd.write(wd2)
	lcd.goto(0,3)
	lcd.write(datetime.now().strftime('%m/%d %w %p %l:%M:%S'))
	lcd.goto(0,2)
	if  network == '000':
		lcd.write('No network')
		#SSTS()
	else:
		lcd.write(wlsd)

#
def Network_layout():   #网络速度
	global wlsd
	global CCC
	#print (wlsd)
	lcd.home()
	lcd.clear()
	lcd.goto(0,0)
	lcd.write('IP:' + CCC[0:14])
	lcd.goto(0,2)
	lcd.write(wlsd)
	lcd.goto(3,1)
	lcd.write("in")
	lcd.goto(10,1)
	lcd.write("out")
	lcd.goto(15,1)
	lcd.write("kb/s")
	lcd.goto(0,3)
	lcd.write(datetime.now().strftime('%m/%d %w %p %l:%M:%S'))
#
def reload_layout():   #重载程序
	global reload
	global exit_flag
	if exit_flag != 1:
		lcd.clear()
		lcd.goto(3,1)
		if reload <= 5:
			lcd.write('reload ?  ' + str(reload))
		else:
			lcd.write('reload ?')


def main():
	global lcd
	global layout
	global exit_flag
	global errors
	thread.start_new_thread(Key_Daemon,())
	RE_welcome = 0
	errors = 0
	lcd = LCD()

	while(True):
		try:
			if errors == 0:
				lcd = LCD()
				#lcd_echo(lcd)
				
				if (RE_welcome != 0):  #re welcome
					if (RE_welcome < 6):
						RE_welcome = 0
					if (RE_welcome > 5):
						Loading()
						RE_welcome = 0

				if layout == 1:
					main_layout()		#主程序界面
					sleep(0.3)
					lcd.goto(19,2)
					lcd.write(' ')

				elif layout == 2:
					Network_layout()
					sleep(0.9)

				elif layout == 0:
					reload_layout()
					sleep(0.9)




		except KeyboardInterrupt:
			exit_flag = 1
			sleep(1)
			lcd.clear()
			lcd.goto(0,1)
			lcd.write("Program End =w=")
			lcd.goto(0,2)
			lcd.write(datetime.now().strftime('%m/%d %w %p %l:%M:%S'))
			lcd.set_brightness(10)
			lcd.close()
			print ('\nProgram End =w=')
			break
		except:
			errors = 1
			sleep(5)
			while errors != 0:
				USB = os.popen('lsusb')
				A = USB.read()
				#print A
				if (A.find("lcd2usb")==-1):
					print ('NO device!')
					errors = 1
				else:
					print ('ok')
					errors = 0
				
		

wd2=''
wlsd=''
network=''
layout = 1




thread.start_new_thread(DHT,())
thread.start_new_thread(Network_Availability,())
thread.start_new_thread(Network_speed,())

print ('ok')
sleep(2)


if __name__ == '__main__':
	try:
		print ('LCD runing.....'+str(os.getpid()))
		main()

	except:
		exit_flag = 1
		print ('\nProgram ERROR! QAQ')


