#!/bin/bash

VOLUME_NAME="AI-models"
if ! docker volume inspect "$VOLUME_NAME" > /dev/null 2>&1; then
    echo "Volume $VOLUME_NAME doesn't exist. Creating..."
    docker volume create "$VOLUME_NAME"
fi