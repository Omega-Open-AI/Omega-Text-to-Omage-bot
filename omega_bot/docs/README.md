# Omega Text-to-Image Bot

## Overview

Omega Text-to-Image Bot is a Python-based application that converts text prompts into images using advanced machine learning models. The bot is designed to be deployed in various environments using Docker.

## Features

- Converts text prompts to images.
- Supports various image generation models.
- Easy configuration and deployment with Docker.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Omega-Open-AI/Omega-Text-to-Image-bot.git
    cd Omega-Text-to-Image-bot
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Running the Bot

1. Create a `.env` file from the example:
    ```sh
    cp .env.example .env
    ```

2. Update the `.env` file with your configuration.

3. Run the bot:
    ```sh
    python -m src.bot
    ```

### Running with Docker

1. Build the Docker image:
    ```sh
    docker-compose build
    ```

2. Run the Docker container:
    ```sh
    docker-compose up
    ```

## Contributing

Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
