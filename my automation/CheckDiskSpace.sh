#!/bin/bash
CURRENT=$(df / | grep / | awk '{ print $5}' | sed 's/%//g')
THRESHOLD=90

if [ "$CURRENT" -gt "$THRESHOLD" ] ; then
	echo "sending email!";
	/usr/local/bin/sendEmail  -f PROTEX@companydomain-t rahul@xyz.com-s ip addr -u "Disk Space LOW!" -m "Your root partition remaining free space is critically low. Used: $CURRENT%";
fi
