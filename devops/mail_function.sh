#!/bin/bash

FROM_ADDRESS=afekuchris@gmail.com
TO_ADDRESS=christopher.afeku@dreamoval.com
SUBJECT="Hello World"
BODY="This is a test"
APP_TOKEN=abnwzvltrgwwtooq

function mail(){
    sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 
}

mail


