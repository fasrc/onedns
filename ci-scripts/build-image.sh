#!/bin/sh
set -e
DOCKER_IMAGE_TAG=${CI_BUILD_REF_NAME}
if [ ${DOCKER_IMAGE_TAG} == "master" ]; then
    DOCKER_IMAGE_TAG="latest"
fi
docker login -u gitlab-ci-token -p $CI_BUILD_TOKEN $CI_REGISTRY
docker build -t $CI_REGISTRY_IMAGE:${DOCKER_IMAGE_TAG} .
docker push $CI_REGISTRY_IMAGE:${DOCKER_IMAGE_TAG}
