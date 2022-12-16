import RPi.GPIO as GPIO
from time import sleep

import config as cf

GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)
GPIO.setup(cf.PicoGPIO, GPIO.OUT) 

GPIO.output(cf.PicoGPIO, cf.PicoOff) 
input('Return to turn Pico on:')
GPIO.output(cf.PicoGPIO, cf.PicoOn) 
input('Return to turn Pico off:')
GPIO.output(cf.PicoGPIO, cf.PicoOff) 
input('Return to turn Pico on:')
GPIO.output(cf.PicoGPIO, cf.PicoOn) 
