
import os
import pandas as pd
from datetime import datetime

def CheckFlag():
    found = False
    for root, dirs, files in os.walk(os.getcwd()):
       for f in files:
           if f[0:4] == 'Flag': 
               os.remove(f)
               found = True
    return found
    
def CheckOFlag():
    found = False
    t1 = None
    t2 = None
    for root, dirs, files in os.walk(os.getcwd()):
       for f in files:
           if f[0:5] == 'OFlag': 
                df = pd.read_csv(f)
                t1 = datetime.strptime(df.iloc[0]['KeepOnTill'],'%Y/%m/%d %H:%M:%S')
                t2 = datetime.strptime(df.iloc[0]['KeepOffTill'],'%Y/%m/%d %H:%M:%S')
                os.remove(f)
                found = True
    return found, t1, t2
    

