#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e
IMAGE_TAG="bustavo/tracewallet:2.2"
DOCKER_USER="bustavo"

echo " Checking Docker Hub Authentication..."

# Check if user is already logged in, otherwise prompt for password safely
if ! docker system info | grep -q "Username: $DOCKER_USER"; then
    echo "Not logged in as $DOCKER_USER. Please authenticate:"
    docker login -u "$DOCKER_USER"
else
    echo "✅ Already authenticated as $DOCKER_USER"
fi

echo -e "\n=========================================="
echo "🏗️  Building Multi-Platform Docker Image..."

# Execute the specific amd64 build command
docker build --platform linux/amd64 -t "$IMAGE_TAG" .

echo "🚀 Pushing Image to Docker Hub..."

# Push the newly built image tag to your repository
docker push "$IMAGE_TAG"

echo "Image pushed successfully!"