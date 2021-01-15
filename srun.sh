#!/bin/sh
#docker stop twitterapi
#docker rm twitterapi
#docker container rm twitterapi
#./docker_twitterapi.py
#docker stop twitterapi
#docker rm twitterapi
#DOCKER_REGISTRY=${DOCKER_REGISTRY:-396648463862.dkr.ecr.eu-west-1.amazonaws.com}
#DOCKER_REGISTRY=${DOCKER_REGISTRY:-us.icr.io/tensortest}
#$(aws ecr get-login --no-include-email --region eu-west-1)
#ibmcloud cr login
#docker build --pull -t "$DOCKER_REGISTRY/insikt-backend-twitterapi:latest" .
docker build --pull -t "restx2020:latest" .
#docker push "$DOCKER_REGISTRY/twitterapi:latest"
#docker run -it -P -d --network=staging_webnet --name=twitterapi "$DOCKER_REGISTRY/insikt-backend-twitterapi:latest" sleep 5000
##docker run -it -P -d --network=host --name=twitterapi twitterapi
#docker exec -it  twitterapi bash
