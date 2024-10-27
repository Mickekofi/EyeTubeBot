import logging
import time
import re
from collections import Counter
from collections import defaultdict
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import types

from EyeTube_you_a import extract_youtube_audio_link
from EyeTube_Ig_a import extract_instagram_audio_link
from EyeTube_Face_a import extract_facebook_audio_link
from EyeTube_X_a import extract_twitter_audio_link
from EyeTube_Lin_a import extract_linkedin_audio_link
from EyeTube_Snap_a import extract_snapchat_audio_link
from EyeTube_am import extract_audiomack_audio_link
from EyeTube_you import download_youtube_video
from EyeTube_Ig import download_instagram_content
from EyeTube_X import download_twitter_video
from EyeTube_Snap import download_snapchat_video
from EyeTube_Face import download_facebook_video
from EyeTube_Lin import download_linkedin_video

import subprocess
from update_checker import UpdateChecker

logging.basicConfig(level=logging.INFO)



print("Welcome to EyeTubeBot For Git Developers!.\n📌 Note, this is Version(1.0.1) of this program.\nWhich gives you Capability to automate the internet downloading videos,movies and extracting audios\n\n\nFind picTuneBot on github for the Image Processing Capability https://github.com/Mickekofi/picTuneBot/tree/master \n\n  Check for updates in the bot chat using the command `/update` which keeps you updated on the current upload work.\n\n We shall implement the full (Version 3.0) development here if we reach our target financial support funds from the Public... for the mean time \n\nplease report any bug or issue on github issues\nTry Our more Matured automated Model(Version 3.0.0) combined with more automated features like Image Processing Features plus grabing detailed Information about a specific internet and social media link, Website legit detection etc..Try Today!    https://t.me/EyeTubeAiBot \n\n")



print("Lets start EyeTubeBot Version(101)...\n")

admin = input("Please enter your name 👉 : ")

TOKEN = input("\nPlease enter your Telegram API token 👉 : ")

# Check if the token was provided
if not TOKEN:
    print("❓You provided No API token.\n\n Shuting down/Exiting...")
    exit(1)

try:
    bot = telebot.TeleBot(TOKEN)
    print("Bot initialized successfully!")
    
    bot_info = bot.get_me()
    print(f"Bot Username: {bot_info.username}")
    print("Ready to receive commands.")
    
except Exception as e:
    print(f"Error: Failed to initialize bot. {e}")





#==============================================================================
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




# UPDATE METHODS
#==============================================================================
update_checker = UpdateChecker("https://raw.githubusercontent.com/Mickekofi/EyeTubeBot")

@bot.message_handler(commands=['check_update'])
def check_updates(message):
    """Check for updates and notify the user."""
    chat_id = message.chat.id

    try:
        latest_version = update_checker.get_latest_version()
        local_version = update_checker.get_local_version()

        if latest_version is None:
            bot.send_message(chat_id, "Failed to fetch the latest version. Please try again later.")
        elif local_version != latest_version:
            bot.send_message(chat_id, f"📌 A new version ({latest_version}) is available!")
            bot.send_message(chat_id, "⬆️ Please update your bot by typing /update.")
        else:
            bot.send_message(chat_id, "✅ Your bot is up to date.")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred while checking for updates: {e}")


@bot.message_handler(commands=['update'])
def update_bot(message):
    """Handle the bot update process."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Starting the update process...")

    try:
        subprocess.run(["git", "pull", "origin", "master"], check=True)
        
        latest_version = update_checker.get_latest_version()
        
        if latest_version:
            update_checker.update_local_version(latest_version)
            
            markup = InlineKeyboardMarkup()
            update_button = InlineKeyboardButton("🎁 Check What is Newly Packed for you", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/update.md")
            markup.add(update_button)
            
            bot.send_message(chat_id, f"✅ Bot updated successfully! Version: {latest_version}\n\nPlease Retart it to take effect", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Update completed, but failed to fetch the latest version. Please check manually.")
    except subprocess.CalledProcessError as e:
        bot.send_message(chat_id, f"Failed to update the bot: {e}")
    except Exception as e:
        bot.send_message(chat_id, f"An unexpected error occurred: {e}")


#STEP 1
#==============================================================================
# Function to check if the these Platform URL are valid links using the regex module to find sequences of user's input string link that match a pattern in the official platform URL string 
# Function to check if it's a valid AudioMack link
def is_valid_audiomack_url(url):
    audiomack_regex = re.compile(r'(https?://)?(www\.)?audiomack\.com/.+/song/.+')
    return audiomack_regex.match(url)


def is_valid_youtube_url(url):
    youtube_regex = re.compile(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+')
    return youtube_regex.match(url)

def is_valid_instagram_url(url):
    instagram_regex = re.compile(r'(https?://)?(www\.)?instagram\.com/.+')
    return instagram_regex.match(url)

def is_valid_twitter_url(url):
    twitter_regex = re.compile(r'(https?://)?(www\.)?(twitter|x)\.com/.+/status/.+')
    return twitter_regex.match(url)

def is_valid_facebook_url(url):
    facebook_regex = re.compile(r'(https?://)?(www\.)?(facebook|fb)\.com/.+')
    return facebook_regex.match(url)

def is_valid_linkedin_url(url): 
    linkedin_regex = re.compile(r'(https?://)?(www\.)?linkedin\.com/(posts|feed|in/.+/detail/recent-activity)/.+')
    return linkedin_regex.match(url)

def is_valid_snapchat_url(url):
    snapchat_regex = re.compile(r'(https?://)?(www\.)?(snapchat\.com/t/.+|snapchat\.com/add/.+|snapchat\.com/discover/.+|snapchat\.com/spotlight/.+)')
    return bool(snapchat_regex.match(url))



# WELCOME START
#==============================================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    # Creating buttons
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/Help')
    itembtn2 = telebot.types.KeyboardButton('/About')
    itembtn3 = telebot.types.KeyboardButton('/check_update')
    itembtn4 = telebot.types.KeyboardButton('/update')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.reply_to(message, f"🕹 {bot_info.username} is Operated by {admin} as the Developer.\n\nPaste your Social Media Movie, Audio or Video Link here?", reply_markup=markup)

#============================================================================================
#About
@bot.message_handler(commands=['About'])
def open_about_command(message):
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()

    # Create 4 buttons with different links
    button1 = types.InlineKeyboardButton(text="Learn about EyeTubeBot Version(101)", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_Dev/Documentation.md")
    button4 = types.InlineKeyboardButton(text="👥 Who are We", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_End_User_/Who_are_we.md")
    button5 = types.InlineKeyboardButton(text="What is in for this Update", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_Dev/update.md")
    
    keyboard.add(button1)
    keyboard.add(button4)  # Adding the other two buttons side by side
    keyboard.add(button5)
    # Send the message with the inline keyboard
    bot.send_message(message.chat.id, "About Info", reply_markup=keyboard)

@bot.message_handler(commands=['Help'])
def open_link_command(message):
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="✅ Help", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_Dev/Documentation.md")
    button2 = types.InlineKeyboardButton(text="❓ What Can EyeTubeBot Do", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_Dev/update.md")

    keyboard.add(button1)
    keyboard.add(button2)
    
    # Send a message with the inline keyboard
    bot.send_message(message.chat.id, '''💁🏻 Explore How to Use EyeTubeB👁t Core(beta)?\n
                click any!''', reply_markup=keyboard)








#STAGE 2
#==============================================================================
# bot to handle the user's message and check if the user's message is a valid link and then send the user a message to wait while the bot is processing the link using the created handle platform function
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
    else:
        bot.reply_to(message, "Sorry, this link is not valid😢")
        #open the start command automatically withot the user typing it or clicking on the start button
        send_welcome(message)
    











#STAGE 4b
#==============================================================================
#This is Where the platform handle functions is defined with two conditions or Roads and checks the string link again if the user wants to download the audio(-a) or video(default) of the link. It then sends the users choice on the right path to the respective "send_audio_link" or "send_video_link" function for further processing and extraction of the download link
# Handle the AudioMack URL
def handle_audiomack_url(message, url):
    bot.reply_to(message, "AudioMack only supports audio downloads. Please wait while I fetch the link...")
    send_audiomack_audio(message, url)

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
        download_url = download_youtube_video(url)
        
        if download_url:
            bot.reply_to(message, f"Here is your download link: {download_url}\n\n.")
        else:
            bot.reply_to(message, "Failed to generate the download link. Please check the URL and try again.")


def handle_instagram_url(message, url):

    if ' -a' in url:
        bot.reply_to(message, "Generating audio download link...")
        send_instagram_audio(message, url.replace(' -a', '').strip())
    else:
        bot.reply_to(message, "Downloading Instagram video. Please wait...")


        try:
            download_url = download_instagram_content(url)
            if download_url:
                bot.reply_to(message, f"Here is your download link: {download_url}\n\n.")
            else:
                bot.reply_to(message, "Failed to generate the download link.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")
        
def handle_twitter_url(message, url):
    if ' -a' in url:
        bot.reply_to(message, "Generating audio download link...")
        send_twitter_audio(message, url.replace(' -a', '').strip())
    else:
        bot.reply_to(message, "Generating Twitter video download link. Please wait...")
        try:
            download_url = download_twitter_video(url)
            if download_url:
                bot.reply_to(message, f"Here is your download link: {download_url}\n\n.")
            else:
                bot.reply_to(message, "Failed to generate the download link.")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

def handle_facebook_url(message, url):
    if ' -a' in url:
        bot.reply_to(message, "Generating audio download link...")
        send_facebook_audio(message, url.replace(' -a', '').strip())
    else:
        bot.reply_to(message, "Downloading Facebook video. Please wait...")
        try:
            video_url = download_facebook_video(url)
            bot.reply_to(message, f"Here is your download link: {video_url}\n\n.")
        except Exception as e:
            bot.reply_to(message, f"Failed to download video: {e}")

def handle_linkedin_url(message, url):
    if ' -a' in url:
        bot.reply_to(message, "Generating audio download link...")
        send_linkedin_audio(message, url.replace(' -a', '').strip())
    else:
        bot.reply_to(message, "Downloading LinkedIn video. Please wait...")
        try:
            logging.info(f"Received LinkedIn URL: {url}")  # Debugging line    
            video_url = download_linkedin_video(url)
            if video_url:
                bot.reply_to(message, f"Here is your download link: {video_url}\n\n.")
            else:
                bot.reply_to(message, "Sorry, something went wrong while generating the download link.")
        except Exception as e:
            logging.error(f"Error while downloading LinkedIn video: {e}")
            bot.reply_to(message, "An error occurred while processing your request. Please try again later.")


def handle_snapchat_url(message, url):
    if ' -a' in url:
        bot.reply_to(message, "Generating audio download link...")
        send_snapchat_audio(message, url.replace(' -a', '').strip())
    else:
        bot.reply_to(message, "Downloading Snapchat video. Please wait...")
        try:
            video_url = download_snapchat_video(url)
            bot.reply_to(message, f"Here is your download link: {video_url}\n\n.")
        except Exception as e:
            bot.reply_to(message, f"Failed to download video: {e}")





#STAGE 4a
#==============================================================================
#This is where the send_audio_link function is defined to send the user the download link for the audio based on the hard work of the Audio extraction functions called the "extract_platform_audio_link" function which are in their independent files

def send_audiomack_audio(message, url):
    audio_url = extract_audiomack_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your AudioMack download link: {audio_url}\n\n.")
    else:
        bot.reply_to(message, "Failed to extract the audio download link.")


def send_youtube_audio(message, url):
    audio_url = extract_youtube_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your YouTube download link: {audio_url}\n\n.")


def send_instagram_audio(message, url):
    audio_url = extract_instagram_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Instagram download link: {audio_url}\n\n.")

def send_facebook_audio(message, url):
    audio_url = extract_facebook_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Facebook download link: {audio_url}\n\n.")



def send_twitter_audio(message, url):
    audio_url = extract_twitter_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Twitter download link: {audio_url}\n\n.")


def send_linkedin_audio(message, url):
    audio_url = extract_linkedin_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your LinkedIn download link: {audio_url}\n\n.")

def send_snapchat_audio(message, url):
    audio_url = extract_snapchat_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Snapchat download link: {audio_url}\n\n.")








#==============================================================================
@retry_on_failure
def bot_polling():
    bot.polling(none_stop=True, timeout=60)

bot_polling()