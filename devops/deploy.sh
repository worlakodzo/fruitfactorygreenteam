#!/bin/bash

function build_uat(){
    git pull -f origin main
    # cd uat/billing_app
    docker-compose up -d
    # cd ../prod/weight_app
    # docker-compose up -d
}

function build_prod(){
    git pull -f origin main
    cd prod/billing_app
    docker-compose up -d
    cd ../prod/weight_app
    docker-compose up -d
}

build_uat()
# build_prod()