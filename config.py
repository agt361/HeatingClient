from datetime import date, datetime
import pandas as pd

Name = 'Chancel'
#PicoURL = 'http://192.168.68.47'
PicoURL = 'http://192.168.1.47'
PicoGPIO = 8
PicoOff = True
PicoOn = False

TimeOnUntil = datetime(2000,1,1,1,1)
HeatingGPIO = 22
HeatingUp = True
Hysteresis = 0.4
HeatingUpTarget = 24
HeatingDownTarget = 14
HeatingTargetDirection = "Up"
HeatingOn = False
CurrentTemperature = 30
ThermalDrag = 2
Counter = 0
Errors = 0
OverrideOn = datetime(2000,1,1,1,1)
OverrideOff = datetime(2000,1,1,1,1)

WorkingDF = pd.DataFrame(columns=['T0','T2'])

