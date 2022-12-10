#!/bin/bash
#This script is to mount the following directories on this VM
#10.60.107.53:/Backup to /media/NASDevice
#10.60.107.57:/home/blackduck/SDK to /home/blackduck/SDK/
#10.60.107.57:/home/blackduck/automationscripts/ to /home/blackduck/automationscripts/
#10.60.107.57:/home/blackduck/Projects/ to /home/blackduck/Projects/
#10.60.107.57:/home/blackduck/TalandJob/ to /home/blackduck/TalandJob/
#10.60.107.57:/home/blackduck/Taland/ to /home/blackduck/Taland/

SSHHOST1=10.60.107.53
SSHHOST2=10.60.107.57
SSHHOST2PASSWORD=jenkins

MEDIANASDEVICEDIR=/media/NASDevice/
SDKDIR=/home/blackduck/SDK
AUTOSCRIPTSDIR=/home/blackduck/automationscripts/
PROJECTSDIR=/home/blackduck/Projects/
TALANDJOBDIR=/home/blackduck/TalandJob/
TALANDDIR=/home/blackduck/Taland/
PASSWORD=jenkins
USER=jenkinsuser
currentdate=$(date '+%Y-%^b-%d')
starttime=$(date '+%H.%M')
rm -rf /root/scripts/mount-error.out 

echo "------------------------------------Start time of the script:  $currentdate   $starttime--------------------------" >> /root/scripts/mount.out



checkstatus(){
	arg=$1
	laststatus=$2
	if [[ $laststatus -ne 0 ]]
	then
		echo "Mount failed for" $arg >> /root/scripts/mount-error.out
	else
		echo "Mount successful for" $arg >> /root/scripts/mount.out
	fi
}

########Checking and mounting 10.60.107.53:/Backup to /media/NASDevice######################
echo "checking and mounting 10.60.107.53:/Backup to /media/NASDevice" >> /root/scripts/mount.out
if mountpoint -q -- "$MEDIANASDEVICEDIR";
then
	echo "$MEDIANASDEVICEDIR already mounted" >> /root/scripts/mount.out
else
	 mount -t nfs $SSHHOST1:/Backup $MEDIANASDEVICEDIR
	 laststatus=$?
	 checkstatus $MEDIANASDEVICEDIR $laststatus
fi


########Checking and mounting 10.60.107.57:/home/blackduck/SDK to /home/blackduck/SDK/######################
echo "checking and mounting 10.60.107.57:/home/blackduck/SDK to /home/blackduck/SDK/" >> /root/scripts/mount.out

if mountpoint -q -- "$SDKDIR"
then
	echo "$SDKDIR already mounted" >> /root/scripts/mount.out
else
	echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:$SDKDIR $SDKDIR
	laststatus=$?
	echo "last status is $laststatus"  >> /root/scripts/mount.out
	checkstatus $SDKDIR $laststatus
fi



########Checking and mounting 10.60.107.57:/home/blackduck/automationscripts/ to /home/blackduck/automationscripts/######################
echo "checking and mounting 10.60.107.57:/home/blackduck/automationscripts/ to /home/blackduck/automationscripts/" >> /root/scripts/mount.out

if mountpoint -q -- "$AUTOSCRIPTSDIR"
then
        echo "$AUTOSCRIPTSDIR already mounted" >> /root/scripts/mount.out
else
        echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:$AUTOSCRIPTSDIR $AUTOSCRIPTSDIR
        laststatus=$?
	checkstatus $AUTOSCRIPTSDIR $laststatus
fi



########Checking and mounting 10.60.107.57:/home/blackduck/Projects/ to /home/blackduck/Projects/######################
echo "checking and mounting 10.60.107.57:/home/blackduck/Projects/ to /home/blackduck/Projects/" >> /root/scripts/mount.out

if mountpoint -q -- "$PROJECTSDIR"
then
        echo "$PROJECTSDIR already mounted" >> /root/scripts/mount.out
else
        echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:$PROJECTSDIR $PROJECTSDIR
        laststatus=$?
	checkstatus $PROJECTSDIR $laststatus
fi

########Checking and mounting 10.60.107.57:/home/blackduck/TalandJob/ to /home/blackduck/TalandJob/######################
echo "checking and mounting 10.60.107.57:/home/blackduck/TalandJob/ to /home/blackduck/TalandJob/" >> /root/scripts/mount.out

if mountpoint -q -- "$TALANDJOBDIR"
then
        echo "$TALANDJOBDIR already mounted" >> /root/scripts/mount.out
else
        echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:$TALANDJOBDIR $TALANDJOBDIR 
        laststatus=$?
	checkstatus $TALANDJOBDIR $laststatus
fi

########Checking and mounting 10.60.107.57:/home/blackduck/Taland/ to /home/blackduck/Taland/######################
echo "checking and mounting 10.60.107.57:/home/blackduck/Taland/ to /home/blackduck/Taland/" >> /root/scripts/mount.out

if mountpoint -q -- "$TALANDDIR"
then
        echo "$TALANDDIR already mounted" >> /root/scripts/mount.out
else
        echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:$TALANDDIR $TALANDDIR
        laststatus=$? 
	checkstatus $TALANDDIR $laststatus
fi

echo "Testing error" >> /root/scripts/mount.out

if mountpoint -q -- "/tmp/aman"
then
        echo "/home/aman already mounted" >> /root/scripts/mount.out
else
        echo $PASSWORD | sshfs -o allow_other -o password_stdin $USER@$SSHHOST2:/home/bhaskar/ /tmp/aman
        laststatus=$?
        checkstatus "/home/aman" $laststatus
fi


currentdate1=$(date '+%Y-%^b-%d')
stoptime=$(date '+%H.%M')

if [ -f /root/scripts/mount-error.out ]
then
	echo "error while mounting" >> /root/scripts/mount.out
	/usr/local/bin/sendEmail -f "opensource@sita.aero" -t "opensource@sita.aero" -s "mx-atl.sita.aero" -u "Error while mounting drives on JenkinsVm" -a "/root/scripts/mount-error.out" -m < "/root/scripts/mount-error.out"
fi

echo "------------------------------------End time of the script:  $currentdate1   $stoptime--------------------------" >> /root/scripts/mount.out











