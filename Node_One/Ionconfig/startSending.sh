#!/bin/bash
cd ~/MCP3008

/bin/cat <<-EOF > cmds
z 12
d 27
f /home/pi/MCP3008/batterylevel.txt
t /home/sysop/repository/zabbix_sender/batterylevel.txt
m 2
a 0
&
q
EOF

/usr/local/bin/cfdptest cmds &&

cd ~/readings/normalreadings

RPATH="/home/sysop/repository/incoming/"
RHMAC="/home/sysop/repository/incoming/hmac"

for f in readings*.txt; do
 if [[ "$f" == 'readings*.txt' ]]; then
 break
 fi
 echo "---------------- starting cfdp tranfer for $f --------------------"
 cmd="/home/pi/ionconfig/cmds"
 cmdh="/home/pi/ionconfig/cmdsh"
 FILE="/home/pi/readings/normalreadings/$f"
 HFILE="/home/pi/readings/hmacs/hmac$f"

/bin/cat <<-EOF > $cmd
z 12
d 27
f $FILE
t $RPATH$f
m 2
a 0
&
q
EOF

 /usr/local/bin/cfdptest $cmd &&
 echo "cfdptest for $f finished"


/bin/cat <<-EOF > $cmdh
z 12
d 27
f $HFILE
t $RHMAC$f
m 2
a 0
&
q
EOF

 /usr/local/bin/cfdptest $cmdh &&
 sleep 1
done

for g in readings*.txt; do
 if [[ "$g" == 'readings*.txt' ]]; then
 break
 fi
 FILE="/home/pi/readings/normalreadings/$g"
 HFILE="/home/pi/readings/hmacs/hmac$g"
 /bin/mv $FILE /home/pi/readings/normalreadings/processed
 /bin/mv $HFILE /home/pi/readings/hmacs/processed
done

echo "Cfdp File transfer complete"
echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"

cd
