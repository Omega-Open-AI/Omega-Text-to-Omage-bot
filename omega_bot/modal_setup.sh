#!/bin/bash

# Setup script for Modal deployment

# Check if Modal CLI is installed
if ! command -v modal &> /dev/null; then
    echo "Installing Modal CLI..."
    pip install modal-client
fi

# Create Modal secrets from .env file
if [ -f .env ]; then
    echo "Creating Modal secrets..."
    modal secret create omega-bot-secrets .env
else
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and fill in your values."
    exit 1
fi

# Deploy to Modal
echo "Deploying to Modal..."
modal deploy omega_bot/modal/deploy.py

# Set up webhook
echo "Setting up webhook..."
modal run omega_bot/modal/deploy.py::setup_webhook

echo "Deployment complete! Your bot should now be running on Modal.com"
echo "Monitor your deployment at: https://modal.com/apps/omega-text-to-image-bot"
