#!/bin/bash
FROM_ADDRESS="greenteamcicd@gmail.com"
TO_ADDRESS="greenteamcicd@gmail.com"

SUBJECT="CICD DEPLOYMENT"
TEST_SUCCESS_BODY="ATTENTION!!! Test Run passed."
DEPLOYMENT_SUCCESS="Deployment is successful"

FAILED_BODY="ATTENTION!!! Test Run Failed."
APP_TOKEN="ucairqdcrdnvsfbl"


function backup(){
    backup_date="$(date +%Y%m%d%H%M%S)"
    cd /home/ubuntu/ganshmuelgreenteam/billing_app
    docker build -t billing-app:00-SNAPSHOT-$backup_date .
    cd /home/ubuntu/ganshmuelgreenteam/weight_app
    docker build -t weight-app:00-SNAPSHOT-$backup_date .

    # log backup image name
    echo "billing-app:00-SNAPSHOT-$backup_date" >> /home/ubuntu/logs/billing_backup_image_log.txt
    echo "weight-app:00-SNAPSHOT-$backup_date" >> /home/ubuntu/logs/weight_backup_image_log.txt
    
}

function deploy_to_test(){
    echo "Building Test Application From Docker Compose File"
    cd /home/ubuntu/ganshmuelgreenteam/billing_app
    docker-compose -f docker-compose-test.yml build
    docker-compose -f docker-compose-test.yml up -d

    cd /home/ubuntu/ganshmuelgreenteam/weight_app
    docker-compose -f docker-compose-test.yml build
    docker-compose -f docker-compose-test.yml up -d
}

function deploy_to_production(){
    echo "Building Production Application From Docker Compose File"
    cd /home/ubuntu/ganshmuelgreenteam/billing_app
    docker-compose -f docker-compose-production.yml build
    docker-compose -f docker-compose-production.yml up -d
    cd /home/ubuntu/ganshmuelgreenteam/weight_app
    docker-compose -f docker-compose-production.yml build
    docker-compose -f docker-compose-production.yml up -d
}

function kill_test_env(){
    echo "Taking Down Test Application From Docker Compose File"
    cd /home/ubuntu/ganshmuelgreenteam/billing_app
    docker-compose -f docker-compose-test.yml down --remove-orphans
    cd /home/ubuntu/ganshmuelgreenteam/weight_app
    docker-compose -f docker-compose-test.yml down --remove-orphans
}

function run_test_script(){

    echo "#######...Testing Started...########"
    # Run weight test cases
    cd /home/ubuntu/ganshmuelgreenteam/weight_app
    python3 -m pytest -v

    # Run billing test cases
    cd /home/ubuntu/ganshmuelgreenteam/billing_app
    python3 -m pytest -v
    echo "#######...Testing Completed...########"


    if [[ $? == 0 ]]; then
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $TEST_SUCCESS_BODY -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes
        kill_test_env
        deploy_to_production
        sendEmail -f $FROM_ADDRESS  -t $TO_ADDRESS -u $SUBJECT -m $DEPLOYMENT_SUCCESS -s smtp.gmail.com:587 -xu $FROM_ADDRESS  -xp $APP_TOKEN -o tls=yes
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

# 2. Deploy to test environment
deploy_to_test

# Wait for 15 second
# to run test
sleep 15

# 3. Run test function on test environment
run_test_script


