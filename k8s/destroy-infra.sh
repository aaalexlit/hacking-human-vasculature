#!/usr/bin/env bash

REPO=mlzoomcamp-images
DOCKER_IMAGE_TAG=blood-vessel-seg-v1

echo 'Deleting ECR repo and all the images'
aws ecr batch-delete-image \
    --repository-name $REPO \
    --image-ids imageTag=$DOCKER_IMAGE_TAG > /dev/null
aws ecr delete-repository --repository-name $REPO > /dev/null