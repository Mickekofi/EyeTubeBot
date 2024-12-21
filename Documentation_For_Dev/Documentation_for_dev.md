<p align="center">
  <a href="https://t.me/EyeTubeAiBot">
    <img src="https://github.com/Mickekofi/EyeTubeBot/blob/master/logo.png" alt="Logo" width="130">
  </a>
</p>
<h1 align="center"><strong>EyeTubeBot Version (2.0.1)</strong></h1>
<p align="center">
  <a href="https://t.me/possibilityAI">
    <img src="https://img.shields.io/badge/Join-Community-blue.svg" alt="Join Community">
  </a>
  <a href="https://wa.me/233505994829?text=*EyeTubeB👁t_From_Github_User_💬Message_:*%20">
    <img src="https://img.shields.io/badge/Contact-Engineers-red.svg" alt="Contact Engineers">
  </a>
</p>

---

This is the basic **Core (beta)** version (2.0.1), designed for developers who want to automate and modify the process of video and audio downloads from platforms such as YouTube, Instagram, Facebook, Twitter, LinkedIn, Snapchat, and Audiomack, Also Grab detailed collection of information from website and Social medial Content postings

## Highlights

- [Highlights](#highlights)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [⬇️ Download 📽️ Movies / 🎬Reals from a Social Media Platform](#️-download-️-movies--reals-from-a-social-media-platform)
- [🧲 Extract and Download 🔊Audio/music from an Uploaded Video from Youtube](#-extract-and-download-audiomusic-from-an-uploaded-video-from-youtube)
- [🔦 Fetch information from a Social Media Video Upload](#-fetch-information-from-a-social-media-video-upload)
- [⛏️ Dig all Information from a Target Website](#️-dig-all-information-from-a-target-website)
- [👮🏾‍♂️ Detect ✓ \[ Fraud \& Legit Website \]](#️-detect---fraud--legit-website-)
- [Commands](#commands)
- [Update Handling](#update-handling)
- [The Structure \& Flow](#the-structure--flow)
  - [Major Library / Module Imports](#major-library--module-imports)
  - [Error Handling Stage](#error-handling-stage)
  - [Step 1: URL Validation](#step-1-url-validation)
  - [Step 2: Handling User Messages](#step-2-handling-user-messages)
  - [Step 3: Handling Specific Platform Links](#step-3-handling-specific-platform-links)
  - [Step 3a: Downloading YouTube Videos](#step-3a-downloading-youtube-videos)
  - [Step 3b: Downloading YouTube Audio](#step-3b-downloading-youtube-audio)
  - [Bot Polling and Final Setup](#bot-polling-and-final-setup)
- [There is More We are Yet to add here!](#there-is-more-we-are-yet-to-add-here)

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


## ⬇️ Download 📽️ Movies / 🎬Reals from a Social Media Platform

To download a **Movie,Real or any Video** from a Social media Platform, follow the steps below:*

1.  ✓Copy the video link from the social media platform.eg;Youtube,Facebook,Instagram etc.
2.  ✓Paste the link in the bot.

**Bot will automatically detect the link and download the video for you.**

visit the following links to learn how to downloads from these Social platforms:

![Preview](https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_End_User/tutorials.gif)

- [Tutorial Download from Facebook]()

- [Tutorial Download from Instagram]()

- [Tutorial Download from Twitter]()

- [Tutorial Download from Snapchat]()





## 🧲 Extract and Download 🔊Audio/music from an Uploaded Video from Youtube

To download a **Music or Audio** from Youtube, follow the steps below:

1.  ✓Copy the video link from Youtube.
2.  ✓Add the letter **" -a"** at the end of the link.eg;```https://www.youtube.com/watch?v -a```
3.  ✓Paste the link in the bot.

**Bot will automatically detect the link and download the audio for you.**

visit the following links to learn how to downloads from Youtube:

![Preview](https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_End_User/tutorials3.gif)

- [Tutorial Download Music from Youtube]()


## 🔦 Fetch information from a Social Media Video Upload

To extract information from a video uploaded on a social media platform, follow the steps below:

1.  ✓Copy the video link from the social media platform.eg;Youtube,Facebook,Instagram etc.
2.  ✓Add the word **" -info"** at the end of the link.eg;```https://www.youtube.com/watch?v -info```
3.  ✓Paste the link in the bot.

**Bot will automatically detect the link and get all information for you.**


## ⛏️ Dig all Information from a Target Website

To extract all information from a website, follow the steps below:

1.  ✓Copy the website link.
2.  ✓Paste the link in the bot.

**Bot will automatically detect the link and get all information for you.**


## 👮🏾‍♂️ Detect ✓ [ Fraud & Legit Website ]

To detect a **Fraud or Legit Website**, follow the steps below:

1.  ✓Copy the website link.
2.  ✓Paste the link in the bot.

**Bot will automatically detect the website and tell you if it is Fraud or Legit.**

![Preview](https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_End_User/tutorials.gif)

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

### Major Library / Module Imports

Below are the major import in the program

```python
  import yt_dlp
  import logging
  import time
  import re
  from collections import Counter
  from collections import defaultdict
  import telebot
  from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
  from telebot import types
  import subprocess
  from update_checker import UpdateChecker

```

1. import yt_dlp

- The yt_dlp Library is an Advanced Library for Internet automated processes

2. import logging

- Used to inform errors, warnings, and other critical information during the bot’s runtime for debugging purposes.

3. import time

- Used to implement delays (e.g., waiting between retries in case of failures).

4. import re

- We Implemented Regular expressions to validate URLs or text patterns to fit different social media platforms Links.

5. import telebot

- This module is from the PyTelegramBotAPI library.

- it is used to create the bot, handle messages, and interact with Telegram’s API.

6. import subprocess

- Used to run system-level commands, though not extensively in the bot.

7 import update_checker

- this is from the bots logic itself used to check for available updates to the bot and notify the admin if a new version of the bot is available.


### Error Handling Stage

After a successful initialization with a verified Telegram API, We start by implementing an error handler to prevent crashes due to network connection failures or unexpected crushes.

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
```

### Step 1: URL Validation

This step involves validating whether the provided URLs from platforms like Facebook, LinkedIn, or Snapchat are correct using regular expressions. The following are examples of platform-specific URL validation functions:
string. These are a few

```python
def is_valid_facebook_url(url):
    facebook_regex = re.compile(r'(https?://)?(www\.)?(facebook|fb)\.com/.+')
    return facebook_regex.match(url)

def is_valid_linkedin_url(url): 
    linkedin_regex = re.compile(r'(https?://)?(www\.)?linkedin\.com/(posts|feed|in/.+/detail/recent-activity)/.+')
    return linkedin_regex.match(url)

def is_valid_snapchat_url(url):
    snapchat_regex = re.compile(r'(https?://)?(www\.)?(snapchat\.com/t/.+|snapchat\.com/add/.+|snapchat\.com/discover/.+|snapchat\.com/spotlight/.+)')
    return bool(snapchat_regex.match(url))

```

### Step 2: Handling User Messages

When a user sends a message (typically a link), the bot verifies if the link is valid using the above URL validation functions. Based on the type of link, the bot calls the appropriate handler function to process the user's request.

```python
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()
    if is_valid_youtube_url(url):
        handle_youtube_url(message, url)
    elif is_valid_instagram_url(url):
        handle_instagram_url(message, url)
    elif is_valid_twitter_url(url):
        handle_twitter_url(message, url)
    elif is_valid_facebook_url(url):
        handle_facebook_url(message, url)
    elif is_valid_linkedin_url(url):
        handle_linkedin_url(message, url)
    elif is_valid_snapchat_url(url):
        handle_snapchat_url(message, url)
    elif is_valid_audiomack_url(url):
        handle_audiomack_url(message, url)
```


### Step 3: Handling Specific Platform Links

This is Where the platform handle functions is defined with two conditions or Roads and checks the string link again if the user wants to download the audio(-a) or video(default) of the link. It then sends the users choice on the right path to the respective

 "send_audio_link" or "send_video_link" function for further processing and extraction of the download link

```python
def handle_youtube_url(message, url):
        # Determine audio or video download request
        if '-a' in url:
            bot.reply_to(message, "Generating YouTube audio download link...")
            send_youtube_audio(message, url.replace('-a', '').strip())
            return  
        
        # Set default quality
        quality = 'best'
        
        # Check for quality options in the URL
        if '-l' in url:
            quality = 'worst'
            url = url.replace('-l', '').strip()
        elif '-h' in url:
            quality = 'best' 

        bot.reply_to(message, "Generating YouTube video download link. Please wait...")
        
        # Call the download function
        download_url = download_youtube_video(url, quality)
        
        if download_url:
            bot.reply_to(message, f"Here is your download link: {download_url}\n\n.")
        else:
            bot.reply_to(message, "Failed to generate the download link. Please check the URL and try again.")
```


### Step 3a: Downloading YouTube Videos

Here’s how YouTube video links are processed using the yt_dlp library:

```python
import yt_dlp
import logging

def download_youtube_video(url, quality='best'):
    try:
        # Define options for yt_dlp
        ydl_opts = {
            'format': f'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if quality == 'best' else 'worst',
            'outtmpl': '%(title)s - %(uploader)s - %(upload_date)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,  # Suppresses output to speed up processing
        }

        # Start the yt_dlp extraction
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            # Log available formats for debugging

            # Find video format (with or without audio)
            video_format = None
            audio_format = None

            # Filter video formats with valid height
            video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height') is not None]
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('abr') is not None]

            # Get the best video format based on quality
            if quality == 'best':
                video_format = max(video_formats, key=lambda f: f.get('height', 0), default=None)
                audio_format = max(audio_formats, key=lambda f: f.get('abr', 0), default=None)
            else:
                video_format = min(video_formats, key=lambda f: f.get('height', 0), default=None)
                audio_format = min(audio_formats, key=lambda f: f.get('abr', 0), default=None)

            if video_format:
                video_url = video_format['url']
            else:
                return None
    
            if audio_format:
                audio_url = audio_format['url']
                return {"video :": video_url, "audio_url":"Add '-a' to the link for only audio" } # I have replaced "audio_url" variable with a message to add '-a' to the link for only audio
            else:
                logging.warning("No suitable audio format found.")
                return {"video_url": video_url, "audio_url": None}

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Download error: {e}")
        return None
    except yt_dlp.utils.ExtractorError as e:
        logging.error(f"Extractor error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return None
```

### Step 3b: Downloading YouTube Audio

If the user wants only the audio, the bot generates an audio download link:

```python
import yt_dlp
#Step 3a
def extract_youtube_audio_link(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = next((f['url'] for f in info_dict['formats'] if f['ext'] == 'm4a' or f['ext'] == 'webm'), None)
    
    return audio_url

```

### Bot Polling and Final Setup

Finally, the bot is set to continuously poll Telegram for new messages:

```python 

#==============================================================================
@retry_on_failure
def bot_polling():
    bot.polling(none_stop=True, timeout=60)

bot_polling()
```

## There is More We are Yet to add here!