import datetime
import time

#Files made after execution of this module are hmacs_date.txt and reads_date.txt

def zabbix_sender(thefile):
    datetxt = thefile[-14:]
    date=datetxt.strip('.txt')
    f=open('vreadings_{}'.format(datetxt), 'r')
    for line in f:
        a = line.split()
        g=open('zabbixreads_{}'.format(datetxt),'a')
        if (a[0] == 'Empty'):
            g.write(" ")
        else:
            if (a[0] == 'Conductivity'):
                dt=(date+" "+a[4])
                ut=time.mktime(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple())
                sut=str(ut).split(".")[0]
                g.write('Zabbix_Server comp {} "{}"\n'.format(sut,line.split("\n")[0]))
            if(a[3] == 'Temperature' ):
                dt=(a[1]+" "+a[2])
                ut=time.mktime(datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").timetuple())
                sut=str(ut).split(".")[0]
                g.write('Zabbix_Server temp {} {}\n'.format(sut,a[4]))
                g.write('Zabbix_Server cond {} {}\n'.format(sut,a[6]))
        g.close()
    e=open('hmaclog_{}'.format(datetxt),'r')
    for hm in e:
        h=open('zabbixhmacs_{}'.format(datetxt), 'a')
        s='Zabbix_Server hmac "{}"\n'.format(hm.split("\n")[0])
        h.write(s)
        h.close()
    return(datetxt)

