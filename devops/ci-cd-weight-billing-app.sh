#!/bin/bash
#create cicd gmail account
FROM_ADDRESS="enter cicd send email address here"
#create group cicd email group for members
TO_ADDRESS="enter cicd receive email address here"

SUBJECT="enter email subject here"

SUCCESS_BODY="Enter success message body here"

FAILED_BODY="Enter failure message body here"

# Login as cicd account at https://myaccount.google.com/ and create an app token under "Security" >> "Signing in to google" >> "App Passwords"
APP_TOKEN="enter security token here"

# 1. Fetch the latest code from remote
# git pull -f origin main
echo "Starting pulling green team weight and billing app repo"
git pull -f origin main
echo "Done pulling green team weight and billing app repo"



function deploy_to_test(){

}

function run_test_script(){
    if [[ $? == 0 ]]; then
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $SUCCESS_BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 
    else 
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $FAILED_BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 

}

function deploy_to_production(){
    echo "Building Production Application From Docker Compose File"
    cd ../billing_app
    docker-compose up -d
    cd ../billing_app
    docker-compose up -d

}


# function send_mail(){
#     sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 

# }







