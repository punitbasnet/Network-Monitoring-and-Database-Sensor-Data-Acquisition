import glob
import datetime
import time
import os

from verify import verify
from zabbix_sender import zabbix_sender

for thefile in glob.glob('/home/sysop/repository/incoming/readings*.txt'):
    print(thefile[-14:])
    datetxt=verify(thefile)
    #print(thefile)
    os.rename(thefile, '/home/sysop/repository/done/readings_{}'.format(datetxt))
    os.rename('/home/sysop/repository/incoming/hmacreadings_{}'.format(datetxt), '/home/sysop/repository/done/hmacreadings_{}'.format(datetxt))
    vfile=zabbix_sender(thefile)
    #print(vfile)
    os.rename('vreadings_{}'.format(vfile), '/home/sysop/repository/verified/vreadings_{}'.format(vfile))
    os.rename('zabbixreads_{}'.format(vfile), '/home/sysop/repository/zabbix_sender/zabbixreads_{}'.format(vfile))
    os.rename('zabbixhmacs_{}'.format(vfile), '/home/sysop/repository/zabbix_sender/zabbixhmacs_{}'.format(vfile))
    os.rename('hmaclog_{}'.format(vfile), '/home/sysop/repository/verified/hmaclog_{}'.format(vfile))
    os.rename('breadings_{}'.format(vfile), '/home/sysop/repository/verified/breadings_{}'.format(vfile))
