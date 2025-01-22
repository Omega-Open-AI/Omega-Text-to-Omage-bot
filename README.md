<div align="center">
  <img src="docs/assets/omega-bot-logo.png" alt="Omega Bot Logo" width="200"/>

  # 🤖 Omega Text to Image Bot
  
  <p align="center">
    <strong>Transform Your Words into Art with AI 🎨</strong>
  </p>

  [![CI/CD Pipeline](https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot/actions/workflows/ci.yml)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
  [![Docker](https://img.shields.io/badge/docker-supported-brightgreen.svg)](https://www.docker.com/)
  [![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
</div>

## 🌟 Features

- 🎨 **AI-Powered Image Generation**: Transform text descriptions into stunning images using state-of-the-art AI models
- 🤖 **Telegram Integration**: Easy-to-use interface through Telegram messenger
- ⚡ **Fast Processing**: Optimized for quick image generation with GPU support
- 🛡️ **Safe & Secure**: Built-in content filtering and rate limiting
- 🎯 **Multiple Models**: Support for various Stable Diffusion models
- 📊 **Monitoring**: Integrated metrics and health monitoring
- 🔄 **Scalable**: Docker support for easy deployment and scaling

## 🚀 Quick Start

### 🐳 Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot.git
cd Omega-Text-to-Omage-bot

# Set up environment variables
cp .env.example .env
# Edit .env with your Telegram Bot Token

# Start the bot
docker-compose up -d
```

### 🐍 Manual Installation

```bash
# Clone the repository
git clone https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot.git
cd Omega-Text-to-Omage-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Telegram Bot Token

# Run the bot
python -m omega_bot
```

## 💡 Usage

1. **Start the Bot**: Send `/start` to begin interaction
2. **Generate Images**: Use `/generate` followed by your description
   ```
   /generate a majestic lion in a sunset savanna
   ```
3. **View Settings**: Use `/settings` to see current configuration
4. **Get Help**: Send `/help` for command list and tips

## 🛠️ Configuration

The bot can be configured through various files in the `config` directory:

- `settings.yaml`: General bot settings
- `models.json`: AI model configurations
- `logging.yaml`: Logging settings

Example `settings.yaml`:
```yaml
bot:
  name: "Omega Text to Image Bot"
  max_image_size: 1024
  supported_formats: ["png", "jpg"]

rate_limit:
  max_requests_per_minute: 5
  max_requests_per_day: 50
```

## 🔧 Development

### Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (recommended)
- Docker (optional)

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linters
black .
flake8 .
mypy omega_bot/
```

## 🏗️ Project Structure

```
omega_bot/
├── config/             # Configuration files
├── omega_bot/          # Main package
│   ├── core/           # Core functionality
│   ├── data/           # Data management
│   ├── security/       # Security features
│   └── utils/          # Utilities
├── tests/              # Test suite
└── docs/               # Documentation
```

## 📈 Monitoring

The bot includes Prometheus metrics at:
- `http://localhost:9090/metrics`

Key metrics:
- Image generation time
- Request rates
- Error rates
- Model usage statistics

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m "Add some AmazingFeature"`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Stable Diffusion](https://stability.ai/) for the AI models
- [python-telegram-bot](https://python-telegram-bot.org/) for Telegram integration
- [Hugging Face](https://huggingface.co/) for model hosting

## 📞 Support

- 📚 [Documentation](docs/README.md)
- 🐛 [Issue Tracker](https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot/issues)
- 💬 [Discussions](https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot/discussions)

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/Omega-Open-AI">Omega-Open-AI</a></sub>
</div>
