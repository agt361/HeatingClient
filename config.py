from datetime import date, datetime
import pandas as pd

Name = 'Chancel'
#PicoURL = 'http://1.1.1.1'
PicoURL = 'http://1.1.1.1'
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

