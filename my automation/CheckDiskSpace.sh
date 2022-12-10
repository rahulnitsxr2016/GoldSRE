#!/bin/bash
CURRENT=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')
THRESHOLD=90

if [ "$CURRENT" -gt "$THRESHOLD" ] ; then
	echo "sending email!";
	/usr/local/bin/sendEmail  -f PROTEX@sita.aero -t cathal.mclaughlin@sita.aero,gary.doherty@sita.aero -s 57.250.243.10 -u "Disk Space LOW!" -m "Your root partition remaining free space is critically low. Used: $CURRENT%";
fi
