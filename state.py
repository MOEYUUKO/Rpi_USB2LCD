#!/usr/bin/python2.7
#-*- coding: UTF-8 -*-
import commands
import os
import thread
import time
import random
import sys
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
	mem_total = round(float(lines[0].split()[1]) / 1024, 1)
	mem_free = round(float(lines[2].split()[1]) / 1024, 1)
	men_used = round((mem_free/mem_total)*100)
	return men_used
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