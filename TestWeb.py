import os
import sys
import requests
import re
import RPi.GPIO as GPIO
from time import sleep

def get_html(website_url):
	er = 0
	headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; PIWEBMON)',
        'Cache-Control': 'no-cache' }
	try: response = requests.get(website_url, headers=headers, timeout = 10)
	except Exception as e: 
		return -1, " Error"

	if (response.status_code < 200 or response.status_code > 299):
		return -1, "Error"

	return 1, response.text

def main(i):
	website_status, html = get_html("http://192.168.1.47")

	if website_status == -1:
		print("Error while fetching")
	else:
		t = float((re.findall(':.*:|$', html)[0]).strip(":"))
		print (i, t)


GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(8, GPIO.OUT) 

#GPIO.output(8, True) 
#sleep(8)
GPIO.output(8, False) 
sleep(15)

i = 0
while True: 
	main(i)
	i += 1
	sleep(1)



