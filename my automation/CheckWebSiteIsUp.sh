#! /usr/bin/sh
sendemail=/usr/local/bin/sendEmail
sendfrom="protexlive@sita.aero"
senderaddress="cathal.mclaughlin@sita.aero"
sendto="opensource@sita.aero"
smtpserver="mx-atl.sita.aero"
emailsubject="FAILURE: Website - ""$2""{""$1""} is not running!"

rc=$(curl -s -o "/dev/null" $1)
rc=$?; 
if [[ $rc != 0 ]]; then 
	 echo "Error occurred getting URL $1:"
	 if [ "$rc" -eq "6" ]; then
		 echo "Unable to resolve host"
		 $sendemail -f $sendfrom -t $sendto -s $smtpserver -u "$emailsubject"  -m "Website check failed :  Unable to resolve host : $1" ;
	 fi
	 if [ "$rc" -eq "7" ]; then
		 echo "Unable to connect to host"
		 $sendemail -f $sendfrom -t $sendto -s $smtpserver -u "$emailsubject" -m "Website check failed :  Unable to connect to host : $1" ;
	 fi
	exit $rc; 
fi
