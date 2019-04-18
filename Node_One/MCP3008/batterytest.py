import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import datetime

# Software SPI configuration:
#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:

SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
count = 0
avgread = 0

while (count !=5):
    read = mcp.read_adc(7)
    avgread = avgread + read
    count +=1
    time.sleep(30)
avgread = int(avgread/5)
print (avgread)

current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(current_time)

o=open('batterylevel.txt', 'w')

if (avgread < 530):
    o.write('Zabbix_Server battery "The system has less than 1 HOUR of battery left at {}"'.format(current_time))
if (avgread < 560 and avgread > 530):
    o.write('Zabbix_Server battery "There is approximately 5 HOURS of battery left at {}"'.format(current_time))
if (avgread < 575 and avgread > 560):
    o.write('Zabbix_Server battery "There is approximately 10 HOURS of battery left at {}"'.format(current_time))
if (avgread < 580 and avgread > 575):
    o.write('Zabbix_Server battery "There is approximately 20 HOURS of battery left at {}"'.format(current_time))
if (avgread < 590 and avgread > 580):
    o.write('Zabbix_Server battery "There is approximately 30 HOURS of battery left at {}"'.format(current_time))
if (avgread < 595 and avgread > 590):
    o.write('Zabbix_Server battery "There is approximately 40 HOURS of battery left at {}"'.format(current_time))
if (avgread < 600 and avgread > 595):
    o.write('Zabbix_Server battery "There is approximately 50 HOURS of battery left at {}"'.format(current_time))
if (avgread < 610 and avgread > 600):
    o.write('Zabbix_Server battery "There is approximately 60 HOURS of battery left at {}"'.format(current_time))
if (avgread < 615 and avgread > 610):
    o.write('Zabbix_Server battery "There is approximately 70 HOURS of battery left at {}"'.format(current_time))
if (avgread < 620 and avgread > 615):
    o.write('Zabbix_Server battery "There is approximately 80 HOURS of battery left at {}"'.format(current_time))
if (avgread < 630 and avgread > 620):
    o.write('Zabbix_Server battery "There is approximately 90 HOURS of battery left at {}"'.format(current_time))
if (avgread > 630):
    o.write('Zabbix_Server battery "There is more than 90 HOURS of battery left at {}"'.format(current_time))
o.write('\n')
o.close()



