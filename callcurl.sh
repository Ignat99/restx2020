#!/bin/bash

# Thet is script for test TSL connection
curl  -i --cacert s.crt -H "Content-Type: application/json" -X POST -d '{"keywords": "trump bomb", "users": "ak47", "locations": "Madrid", "langs": "en"}' https://curl.aaa.com:8032/keywords
#curl  -k -i --cacert s.crt -H "Content-Type: application/json" -X POST -d '{"keywords": "bomb", "users": "ak47", "locations": "Madrid", "langs": "en"}' http://192.168.99.100:8032/keywords

