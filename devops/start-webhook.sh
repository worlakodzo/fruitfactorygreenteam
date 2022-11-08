#!/bin/bash


echo "Starting webhook server..."
webhook -hooks /automation/hooks.json -hotreload -verbose -http-methods post -port 8088