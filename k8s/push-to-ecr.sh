#!/usr/bin/env bash

# GATEWAY_LOCAL_IMAGE_TAGGED=tf-serving-gateway:v001 
# MODEL_LOCAL_IMAGE_TAGGED=tf-serving-model:xception-x86-v1 

# Check if the number of arguments is correct
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 local_image_with_tag"
    exit 1
fi

# Assign the argument to a variable
LOCAL_IMAGE_TAGGED=$1

REPO=mlzoomcamp-images
REGION=$(aws configure get region)
ACCOUNT=$(aws sts get-caller-identity --query "Account" --output text)
ECR_URL=${ACCOUNT}.dkr.ecr.${REGION}.amazonaws.com

PREFIX=${ECR_URL}/${REPO}
TAG=$(echo $LOCAL_IMAGE_TAGGED | sed 's/:/-/g')
REMOTE_URI=${PREFIX}:${TAG}

# Exit the script if any command returns a non-zero status
set -e

echo "Creating ECR repo ${REPO}"

# Check if the repository already exists
if aws ecr describe-repositories --repository-names $REPO 2>&1 | grep -q "RepositoryNotFoundException"; then
    # Repository does not exist, so create it
    aws ecr create-repository --repository-name $REPO > /dev/null
    echo "ECR repository ${REPO} created successfully."
else
    echo "ECR repository ${REPO} already exists."
fi

echo 'Log into ECR with docker'
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_URL

echo 'Tag the image and push to ECR repo'

echo "Tagging existing image with the remote tag ${REMOTE_URI}"
docker tag $LOCAL_IMAGE_TAGGED $REMOTE_URI

echo 'Pushing it to ECR'
docker push $REMOTE_URI
