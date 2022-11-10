#!/bin/bash
#create cicd gmail account
FROM_ADDRESS="greenteamcicd@gmail.com"
#create group cicd email group for members
TO_ADDRESS="greenteamcicd@gmail.com"

SUBJECT="CICD DEPLOYMENT"

TEST_SUCCESS_BODY="ATTENTION!!! Test Run passed."
DEPLOYMENT_SUCCESS="Deployment is successful"

FAILED_BODY="ATTENTION!!! Test Run Failed."

# Login as cicd account at https://myaccount.google.com/ and create an app token under "Security" >> "Signing in to google" >> "App Passwords"
APP_TOKEN="ucairqdcrdnvsfbl"


function backup(){
    backup_date="$(date +%Y%m%d%H%M%S)"
    cd ../billing_app 
    docker build -t billing-app:00-SNAPSHOT-$backup_date .
    cd ../weight_app
    docker build -t weight-app:00-SNAPSHOT-$backup_date .
}

function deploy_to_test(){
    echo "Building Test Application From Docker Compose File"
    cd ../billing_app
    docker-compose build
    docker-compose up -d
    cd ../weight_app
    docker-compose 
    docker-compose up -d
}


function deploy_to_production(){
    echo "Building Production Application From Docker Compose File"
    cd ../billing_app
    docker-compose build
    docker-compose up -d
    cd ../weight_app
    docker-compose 
    docker-compose up -d
}

function run_test_script(){
    echo "#######Testing Started...########"
    # python3 -m pytest -v
    echo "#######Testing Completed...########"
    
    if [[ $? == 0 ]]; then
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $DEPLOYMENT_SUCCESS -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 
        deploy_to_production
        
    else 
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $FAILED_BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes 
    fi
}

# Create a backup of the images.
backup

# 1. Fetch the latest code from remote
# git pull -f origin main
echo "Starting pulling green team weight and billing app repo"
git pull -f origin main
echo "Done pulling green team weight and billing app repo"

deploy_to_test
run_test_script

