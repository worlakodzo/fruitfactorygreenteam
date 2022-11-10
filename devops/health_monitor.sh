#!/bin/bash

weight_endpoint="ec2-18-192-110-37.eu-central-1.compute.amazonaws.com"
billing_endpoint="ec2-18-192-110-37.eu-central-1.compute.amazonaws.com"

function health_check(){
    # checking weight endpoint health status
    nc -zv $weight_endpoint 8081 > temp.txt 2>&1
    cat temp.txt | xargs | awk '{ "date" | getline d; print d " "$0}' >> weight_app_logs.txt
    sleep 5

    # checking billing endpoint health status
    nc -zv $weight_endpoint 8081 > temp.txt 2>&1
    cat temp.txt | xargs | awk '{ "date" | getline d; print d " "$0}' >> weight_app_logs.txt
    sleep 5
}

health_check