#written by YY, 20170408
#record the MAS rate on Bruker AVAMNCE 3 and store the data into file
#the time separation between consecutive measurements is 
#controlled by SLEEP(unit s) and the number of points is determined by
#for loop

#MASRGET will get the MAS rate for MAS II unit and store it 
#as a state parameter

import time
import os,sys

if len(sys.argv)==1:
	sleep_time=5
	num_of_log=50000
else:
	sleep_time=float(sys.argv[1])
	num_of_log=int(sys.argv[2])
	
	
date=time.strftime('_%d_%b_%Y', time.localtime(time.time()))

f=open(('/home/%s/masrate/masrate')%os.getenv('USER')+date,'a')
for i in range(num_of_log):
    ct = XCMD('MASRGET')
    masrate=GETPARSTAT('MASR')
    curr_time=time.strftime('%a, %d %b %Y, %H:%M:%S', time.localtime(time.time()))
    f.write(('time: %s speed: %s')% (curr_time, masrate) + "\n")
    SLEEP(sleep_time)    
f.close()

