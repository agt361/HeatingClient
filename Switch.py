import RPi.GPIO as GPIO
from datetime import date, datetime, timedelta
import os
import shutil
#import plotly.express as px
import pandas as pd
import csv
from time import sleep
from tabulate import tabulate
from threading import Thread
import sys
import subprocess
from math import ceil
import requests
#import urllib.request
import re

import config as cf
#import TemperatureClient as TC
import FileSearch as FS

def GetHTML(url,hdr,val):
	headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        hdr:val,'Cache-Control': 'no-cache' }
	try: response = requests.get(url, headers=headers, timeout = 10)
	except Exception as e: 
		return -1, " Error"
	if (response.status_code < 200 or response.status_code > 299):
		return -1, "Error"
	return 1, response.text

def SetHeating(nf):
	ss = '1' if nf else '0'
	web_status, html = GetHTML(cf.PicoClientURL,'Test',ss)
	cf.Switch = "OK" if web_status == 1 and ss == html[:1] else "Problem"

def TruncateFile(LFile,NewL):
	GhostFile = 'ghost.csv'
	df = (pd.read_csv(LFile)).iloc[-NewL:]

	with open(GhostFile, 'w') as csv_file:
		df.to_csv(path_or_buf=csv_file, index = False)
	shutil.copyfile(GhostFile,LFile)
	
def week_of_month(dt):
    first_day = dt.replace(day=1)
    dom = dt.day
    adjusted_dom = dom + first_day.weekday()
    return int(ceil(adjusted_dom/7.0))
    
def ReadInTemporary():
	FileName = "Temporary.csv"
	df = pd.read_csv(FileName)
	df['DateTime'] = pd.to_datetime(df['DateTime'])
	df['Duration'] = pd.to_datetime(df['Duration']).dt.time
	j = len(cf.WorkingDF)
	for i in range(len(df)):
		t0 = df.iloc[i]['DateTime']
		t1 = df.iloc[i]['Duration']
		t2 = t0 + timedelta(hours = t1.hour, minutes = t1.minute)
		cf.WorkingDF.loc[i+j] = [t0,t2]
    
def BasicDate(x):
	return datetime.combine(x, datetime.min.time())
	
def ReadInPermanent(x):
	gotit = False
	FileName = "Permanent.csv"
	df = pd.read_csv(FileName)
	df['Time'] = pd.to_datetime(df['Time'])
	df['Duration'] = pd.to_datetime(df['Duration']).dt.time
	w = week_of_month(x) - 1
	d = x.weekday() + 1
	j = len(cf.WorkingDF)
	thisdate = BasicDate(x)
	for i in range(len(df)):
		dow = df.iloc[i]['DoW']
		wom = df.iloc[i]['Weeks of Month']
		t1 = df.iloc[i]['Time']
		t11 = df.iloc[i]['Duration']
		try:
			ignoredate = BasicDate(pd.to_datetime(df.iloc[i]['Ignore']))
		except:
			ignoredate = BasicDate(datetime(2000,1,1,1,1))
		if d == dow and wom[w] == 'Y' and thisdate != ignoredate:
			t0 = thisdate + timedelta(hours = t1.hour, minutes = t1.minute)
			t2 = t0 + timedelta(hours = t11.hour, minutes = t11.minute)
			cf.WorkingDF.loc[i+j] = [t0,t2]
			
def EditTimeOnUntil():
	lag = (cf.HeatingUpTarget - cf.CurrentTemperature)/cf.ThermalDrag
	cf.TimeOnUntil = datetime(2000,1,1,1,1)
	for i in range(len(cf.WorkingDF)):
		df = cf.WorkingDF.iloc[i]
		if df['T0'] - timedelta(hours = lag) < datetime.now() and \
		   df['T2'] > datetime.now() and df['T2'] > cf.TimeOnUntil:
		   cf.TimeOnUntil = df['T2']
	
def Thermostat():
	if cf.HeatingUp is True:
		THigh = cf.HeatingUpTarget + cf.Hysteresis
		TLow = cf.HeatingUpTarget - cf.Hysteresis
	else:
		THigh = cf.HeatingDownTarget + cf.Hysteresis
		TLow = cf.HeatingDownTarget - cf.Hysteresis
	if cf.CurrentTemperature > THigh:
		cf.HeatingTargetDirection = 'Down'
		cf.HeatingOn = False
	elif cf.CurrentTemperature >= TLow:
		if cf.HeatingTargetDirection == 'Down':
			cf.HeatingOn = False
		else: cf.HeatingOn = True
	else:
		cf.HeatingTargetDirection = 'Up'
		cf.HeatingOn = True
		print(cf.HeatingOn)
	SetHeating(cf.HeatingOn)


def ReadTemp():
	web_status, html = GetHTML(cf.PicoURL,'x','x')
	if web_status == 1:
		cf.Errors = 0
	else:
		html = "Error:-100:"
		cf.Errors += 1
		if cf.Errors > 9:
			cf.Errors = 0
#			SwitchPicoOffAndOn()
	t = float((re.findall(':.*:|$', html)[0]).strip(":"))
	if t > -20: 
		cf.CurrentTemperature = t
		cf.Sensor = 'OK'
	else:
		cf.CurrentTemperature = cf.HeatingDownTarget
		cf.Sensor = "Problem"
	x = datetime.now()
	xsl = x.strftime("%y/%m/%d %H:%M:%S")
	if cf.HeatingOn: ho = 'Yes'
	else: ho = 'No'
	if cf.HeatingUp: hu = 'Yes'
	else: hu = 'No'
	cf.Counter += 1
	with open("CurrentTemperature.csv", 'w') as f:
		f.write(f"DateTime,Temperature,Heating On,Rads On,Switch,Sensor\n" )
		f.write(f"{xsl},{t},{hu},{ho},{cf.Switch},{cf.Sensor}\n" )
	if (cf.Counter % 120) == 0:
		with open("TemperatureLog.csv", 'a') as f:
			f.write(f"{xsl},{t},{ho}\n" )
	if (cf.Counter % 3600) == 0:
		TruncateFile("TemperatureLog.csv",13333)
		cf.Counter = 0

def ReadInParameters():
	FileName = "System.csv"
	df = pd.read_csv(FileName)
	cf.HeatingUpTarget = float(df.iloc[0]['Target Temperature'])
	cf.HeatingDownTarget = float(df.loc[0]['Background Temperature'])
	cf.Hysteresis = float(df.iloc[0]['Hysteresis'])
	cf.ThermalDrag = float(df.iloc[0]['Thermal Lag'])
	cf.PicoURL = df.loc[0,'PicoIP']
	cf.PicoClientURL = df.loc[0,'PicoClientIP']

def ReadInOverrides():
	FileName = "States.csv"
	f,t1,t2 = FS.CheckOFlag()
	if f:
		if t1 > datetime.now(): cf.OverrideOn = t1
		if t2 > datetime.now(): cf.OverrideOff = cf.TimeOnUntil
		with open(FileName, 'w') as f:
			f.write(f"KeepOnTill,KeepOffTill,Confirmed\n" )
			x = datetime.now()
			xsl1 = t1.strftime("%Y/%m/%d %H:%M:%S")
			xsl2 = t2.strftime("%Y/%m/%d %H:%M:%S")
			xsl3 = x.strftime("%Y/%m/%d %H:%M:%S")
			f.write(f"{xsl1},{xsl2},{xsl3}\n" )
	else:
		df = pd.read_csv(FileName)
		cf.OverrideOn = datetime.strptime(df.iloc[0]['KeepOnTill'],'%Y/%m/%d %H:%M:%S')
		cf.OverrideOff = datetime.strptime(df.iloc[0]['KeepOffTill'],'%Y/%m/%d %H:%M:%S')
	
def Working(name):
	print("/home/pi/shared/"+name)
	os.chdir("/home/pi/shared/"+name)
	ReadInParameters()
	cf.Counter = 0
	cf.Errors = 0
	while True:
		ReadTemp()
		ReadInOverrides()
#		if FS.CheckFlag() == True: 
#			cf.TimeOnUntil = datetime(2000,1,1,1,1)
#			print("Yes")
		cf.WorkingDF = pd.DataFrame(columns=['T0','T2'])
		ReadInParameters()
		ReadInTemporary()
		ReadInPermanent(datetime.now())
		ReadInPermanent(datetime.now() + timedelta(days = 1))
		cf.WorkingDF.sort_values(by=['T0'], inplace=True)
#		print(cf.WorkingDF)
		EditTimeOnUntil()
		if (datetime.now() < cf.TimeOnUntil and cf.TimeOnUntil > cf.OverrideOff) or \
				datetime.now() < cf.OverrideOn:
			cf.HeatingUp = True
		else: cf.HeatingUp = False
		print(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),cf.TimeOnUntil, cf.CurrentTemperature)
		print(cf.HeatingUp,cf.HeatingTargetDirection, cf.HeatingOn)
		print( cf.OverrideOn,cf.OverrideOff)
		Thermostat()
		sleep(5)

Working(sys.argv[1])
