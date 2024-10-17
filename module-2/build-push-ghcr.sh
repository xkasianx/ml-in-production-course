#!/bin/bash

# login to ghcr.io - echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
docker build -t simple-http .   
docker tag simple-http:latest ghcr.io/xkasianx/ml-in-production-course/simple-http:latest
docker push ghcr.io/xkasianx/ml-in-production-course/simple-http:latest 