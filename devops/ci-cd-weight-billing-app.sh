#!/bin/bash

# 1. Fetch the latest code from remote
# git pull -f origin main
echo "Starting pulling green team weight and billing app repo"
git pull -f origin main
echo "Done pulling green team weight and billing app repo"



function deploy_to_test(){

}


function run_test_script(){
    echo "#######Testing Started...########"
    python3 -m pytest -v
    echo "#######Testing Completed...########"
}


function deploy_to_production(){

}











