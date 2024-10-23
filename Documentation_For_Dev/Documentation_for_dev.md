<p align="center">
  <a href="https://t.me/EyeTubeAiBot">
    <img src="https://github.com/Mickekofi/EyeTubeBot/blob/master/logo.png" alt="Logo" width="130">
  </a>
</p>
<h1 align="center"><strong>EyeTubeBot Version (1.0.1)</strong></h1>
<p align="center">
  <a href="https://t.me/possibilityAI">
    <img src="https://img.shields.io/badge/Join-Community-blue.svg" alt="Join Community">
  </a>
  <a href="https://wa.me/233505994829?text=*EyeTubeB👁t_From_Github_User_💬Message_:*%20">
    <img src="https://img.shields.io/badge/Contact-Engineers-red.svg" alt="Contact Engineers">
  </a>
</p>

---

This is the basic **Core (beta)** version (1.0.1), designed for developers who want to automate and modify the process of video and audio downloads from platforms such as YouTube, Instagram, Facebook, Twitter, LinkedIn, Snapchat, and Audiomack.

## Highlights

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Update Handling](#update-handling)
- [The Structure & Flow](#the-structure--flow)

## Features

- Basic link automation mechanism for video and audio downloads.

## Requirements

- **Python 3.7+**
- Libraries:
  - `telebot` (pyTelegramBotAPI)
  - `re`
  - `time`
  - `logging`
  - `subprocess`
  - `update_checker`

- An active **Telegram Bot API Token** from [BotFather](https://t.me/BotFather).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/Mickekofi/EyeTubeBot.git
    cd EyeTubeBot
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Set up your bot with your Telegram API token:
    ```python
    TOKEN = input("Please enter your Telegram API token: ")
    bot = telebot.TeleBot(TOKEN)
    ```
   Get your **Telegram Bot API Token** from [BotFather](https://t.me/BotFather).

2. **Admin Setup**: Enter your name when prompted to personalize the bot's welcome messages.

3. **Error Handling**: The bot retries operations on failures using the `retry_on_failure` decorator.

## Usage

1. **Starting the Bot**: Run the bot by executing:
    ```bash
    python EyeTube_main.py
    ```

2. **Platform Support**:
   - Supported platforms for video/audio extraction:
     - YouTube
     - Instagram
     - Twitter
     - Facebook
     - LinkedIn
     - Snapchat
     - Audiomack

3. **Audio/Video Download**:
   - To download **audio**, append `-a` to the URL.
   - To download **video**, simply paste the URL. The bot will automatically handle the request.
   - For YouTube, specify the video quality using `-h` for high quality or `-l` for low quality (default is high).

## Commands

- `/start`: Starts the bot and presents a basic user interface for interaction.
- `/help`: Provides a link to the bot's documentation.
- `/about`: Displays information about the EyeTubeBot.
- `/check_update`: Checks for available bot updates.
- `/update`: Automatically pulls updates from the GitHub repository.

## Update Handling

EyeTubeBot includes built-in update handling:
1. Use the `/check_update` command to see if a newer version is available.
2. Use the `/update` command to update the bot via a GitHub pull request.

Refer to the [Update Documentation](https://github.com/Mickekofi/EyeTubeBot/blob/master/update.md) for details on new releases.

## The Structure & Flow

After a successful initialization with a verified Telegram API, the bot implements an error handler to prevent crashes due to network connection failures.

```python
# Retry Error Handling
def retry_on_failure(func):
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Error: {e}. Retrying in 5 seconds...")
                time.sleep(20)
    return wrapper
