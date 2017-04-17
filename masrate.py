#written by YY, 20170408
#record the MAS rate on Bruker AVANCE III and store the data into file
#Compatible with Topspin 3.2, which has a Jython compiler
#the time separation between consecutive measurements is
#controlled by SLEEP(unit s) and the number of points is determined by
#for loop.

#MASRGET will get the MAS rate from MAS II unit and store it
#as a state parameter
import time
date=time.strftime(“_%d_%b_%Y”, time.localtime(time.time()))
f=open(“/directory/file”+date,’w’)
for i in range(100):
    ct = XCMD(“MASRGET”)
    masrate=GETPARSTAT(“MASR”)
    curr_time=time.strftime(“%a, %d %b %Y, %H:%M:%S”, time.localtime(time.time()))
    f.write(“time:”+curr_time+” ,speed:”+masrate+”\n”)
    SLEEP(5)
f.close()
