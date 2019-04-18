#!/bin/bash
sudo hwclock -s
echo "$(sudo hwclock -s) Time retained at $(date)" >> /home/pi/deployment/rasclock.log


