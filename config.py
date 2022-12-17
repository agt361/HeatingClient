from datetime import date, datetime
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

NaveUsed = eval(os.getenv('NaveUsed'))
NavePicoIP = os.getenv('NavePicoIP')
NaveClientPicoIP = os.getenv('NaveClientPicoIP')
NaveSwitchLocal = eval(os.getenv('NaveSwitchLocal'))
NaveSensorLocal = eval(os.getenv('NaveSensorLocal'))

ChancelUsed = eval(os.getenv('ChancelUsed'))
ChancelPicoIP = os.getenv('ChancelPicoIP')
ChancelClientPicoIP = os.getenv('ChancelClientPicoIP')
ChancelSwitchLocal = eval(os.getenv('ChancelSwitchLocal'))
ChancelSensorLocal = eval(os.getenv('ChancelSensorLocal'))

Flags = pd.Series( [NavePicoIP, NaveClientPicoIP, ChancelPicoIP, ChancelClientPicoIP, \
                    NaveSwitchLocal, NaveSensorLocal,ChancelSwitchLocal, ChancelSensorLocal], \
            index=['Nave', 'NaveClient', 'Chancel', 'ChancelClient', \
                    'NaveSwitch','NaveSensor','ChancelSwitch','ChancelSensor'])
print(Flags)

Name = 'Chancel'

PicoURL = 'http://1.1.1.1'
PicoClientURL = 'http://1.1.1.1'
PicoGPIO = 8
PicoOff = True
PicoOn = False
Event = ' '

TimeOnUntil = datetime(2000,1,1,1,1)
HeatingGPIO = 22
HeatingUp = True
Hysteresis = 0.4
HeatingUpTarget = 24
HeatingDownTarget = 14
HeatingTargetDirection = "Up"
HeatingOn = False
CurrentTemperature = -100
ThermalDrag = 2
Counter = 0
Errors = 0
OverrideOn = datetime(2000,1,1,1,1)
OverrideOff = datetime(2000,1,1,1,1)

Sensor = 'OK'
Switch = 'OK'

WorkingDF = pd.DataFrame(columns=['T0','T2','Event'])
