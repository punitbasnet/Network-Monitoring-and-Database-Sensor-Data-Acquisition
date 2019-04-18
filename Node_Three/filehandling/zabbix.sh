#!/bin/bash
cd /home/sysop/repository/incoming
for e in hmacreadings*.txt; do
        if [[ "$e" == 'hmacreadings*.txt' ]]; then
                break
        fi
	python3 /usr/bin/code/boss.py &&
	sleep 1
done

cd /home/sysop/repository/zabbix_sender

for d in battery*.txt; do
        if [[ "$d" == 'battery*.txt' ]]; then
                break
        fi
	/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i batterylevel.txt &&
	echo "BATTERY LEVEL REPORTED"
	rm batterylevel.txt
done

for f in zabbixread*.txt; do
	if [[ "$f" == 'zabbixread*.txt' ]]; then 
		break
	fi
 	/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i $f -T &&
	sleep 5
	/bin/mv $f /home/sysop/repository/zabbix_sender/processed
	/bin/echo "READINGS FROM $f SENT TO SERVER ON $(/bin/date)"
done

for g in zabbixhmac*.txt; do
	if [[ "$g" == 'zabbixhmac*.txt' ]]; then
                break
        fi
	/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -i $g &&
	sleep 5
	/bin/mv $g /home/sysop/repository/zabbix_sender/processed
	/bin/echo "HMAC LOGS FROM $g SENT TO SERVER ON $(/bin/date)"
done
cd

