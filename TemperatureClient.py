import urllib.request
import datetime
import time
import RPi.GPIO as GPIO
import re

import config as cf

url = cf.PicoURL

req = urllib.request.Request(url)
def GetTemp():
    while True:
        i = 0
        er = False
        html = "Error:-100:"
        try: html = str(urllib.request.urlopen(req, timeout = 10).read())
        except TimeoutError as e:
            i += 1
        except urllib.error.URLError as e:
            i += 1
        except Exception as e:        
            i += 1
        if i == 3:
            i = 0
            GPIO.output(cf.PicoGPIO, cf.PicoOff) 
            time.sleep(10)
            GPIO.output(cf.PicoGPIO, cf.PicoOn)
            continue
        t = float((re.findall(':.*:|$', html)[0]).strip(":"))
        print(t)
        if t > -20: cf.CurrentTemperature = t
        x = datetime.datetime.now()
        xsl = x.strftime("%y/%m/%d %H:%M:%S")
        with open("/home/pi/shared/TemperatureLog.csv", 'a') as f:
            f.write(f"{xsl},{t}\n" )
        with open("/home/pi/shared/CurrentTemperature.csv", 'w') as f:
            f.write(f"DateTime,Temperature\n" )
            f.write(f"{xsl},{t}\n" )
        
        time.sleep(2)
        
#GetTemp()
    
