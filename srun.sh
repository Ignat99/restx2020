#!/bin/sh
#docker stop restx2020
#docker rm restx2020
#docker container rm restx2020
#./docker_restx2020.py
#docker stop restx2020
#docker rm restx2020
#DOCKER_REGISTRY=${DOCKER_REGISTRY:-396648463862.dkr.ecr.eu-west-1.amazonaws.com}
#DOCKER_REGISTRY=${DOCKER_REGISTRY:-us.icr.io/tensortest}
#$(aws ecr get-login --no-include-email --region eu-west-1)
#ibmcloud cr login
#docker build --pull -t "$DOCKER_REGISTRY/satellogic-backend-restx2020:latest" .
docker build --pull -t "restx2020:latest" .
#docker push "$DOCKER_REGISTRY/restx2020:latest"
#docker run -it -P -d --network=staging_webnet --name=twitterapi "$DOCKER_REGISTRY/satellogic-backend-restx2020:latest" sleep 5000
##docker run -it -P -d --network=host --name=restx2020 restx2020
#docker exec -it  restx2020 bash
