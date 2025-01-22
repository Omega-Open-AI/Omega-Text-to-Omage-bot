"""
Omega Text to Image Bot
A Telegram bot for generating images from text descriptions using AI models.

Author: Omega-Open-AI
Date: 2025-01-22
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="omega-text-to-image-bot",
    version="1.0.0",
    author="Omega-Open-AI",
    author_email="contact@omega-open-ai.com",
    description="A Telegram bot for generating images from text using AI models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Omega-Open-AI/Omega-Text-to-Omage-bot",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Communications :: Chat",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.9.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
            "sphinx>=7.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "omega-bot=omega_bot.core.bot:main",
        ],
    },
    include_package_data=True,
    package_data={
        "omega_bot": [
            "config/*.yaml",
            "config/*.json",
        ],
    },
)
