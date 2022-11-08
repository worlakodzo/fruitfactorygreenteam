#!/bin/bash


echo "Starting webhook server..."
webhook -hooks ./hooks.json -hotreload -verbose -http-methods post -port 8088