import glob
import datetime
import time
import os

#from verify import verify
#from zabbix_sender import zabbix_sender

for thefile in glob.glob('/home/zabbix/repository/readings*.txt'):
 datetxt = thefile.strip('/home/zabbix/')
 datetxt = datetxt.strip('repository/readings_')
 print(datetxt)
 print(thefile)
