import telebot
import types
import yt_dlp
import time
import re
from EyeTube_you_a import extract_youtube_audio_link
from EyeTube_you import download_youtube_video
from EyeTube_Ig_a import extract_instagram_audio_link
from EyeTube_Face_a import extract_facebook_audio_link
from EyeTube_X_a import extract_twitter_audio_link
from EyeTube_Lin_a import extract_linkedin_audio_link
from EyeTube_Snap_a import extract_snapchat_audio_link
from EyeTube_am import extract_audiomack_audio_link
from EyeTube_Ig import download_instagram_content
from EyeTube_X import download_twitter_video
from EyeTube_Snap import download_snapchat_video
from EyeTube_Face import download_facebook_video
import logging
from EyeTube_Lin import download_linkedin_video

import subprocess
from telebot import TeleBot
from update_checker import UpdateChecker

logging.basicConfig(level=logging.INFO)



print("Welcome to EyeTubeB👁t!.\n📌Note, this is just a basic core version of this program.\nTry Our more Matured automated Model with more automated features like all internet and social media links responce, Website legit detection, audio extraction etc..Try Today! 👉  https://t.me/EyeTubeAiBot \n\n")

print("We could had made this a bit advanced and heavy but costs and server resources wont allow, we decided to take alternatives and make it simple and light for you to use.\n\n")
# Prompt the user for the API token
TOKEN = input("Please enter your Telegram API token 👉: ")

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






# Initialize the update checker with your GitHub repo URL
update_checker = UpdateChecker("https://raw.githubusercontent.com/Mickekofi/EyeTubeBot")

@bot.message_handler(commands=['check_update'])
def check_updates(message):
    """Check for updates and notify the user."""
    latest_version = update_checker.get_latest_version()
    local_version = update_checker.get_local_version()

    if latest_version and local_version != latest_version:
        bot.send_message(message.chat.id, f"A new version ({latest_version}) is available!")
        bot.send_message(message.chat.id, "Please update your bot by running `git pull` in your bot's directory.")
    else:
        bot.send_message(message.chat.id, "Your bot is up to date.")

@bot.message_handler(commands=['update'])
def update_bot(message):
    """Handle the bot update process."""
    chat_id = message.chat.id
    bot.send_message(chat_id, "Starting the update process...")
    
    try:
        subprocess.run(["git", "pull"], check=True)
        
        #Remmeber to update the version number after pulling
        update_checker.update_local_version("1.0.0")  # Update with the new version after pulling
        
        
        bot.send_message(chat_id, "Bot updated successfully!")
    except subprocess.CalledProcessError:
        bot.send_message(chat_id, "Failed to update the bot.")


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

#==============================================================================


@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    # Creating buttons
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/Help')
    itembtn2 = telebot.types.KeyboardButton('/About')
    itembtn3 = telebot.types.KeyboardButton('/')
    itembtn4 = telebot.types.KeyboardButton('/')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.reply_to(message, "Welc👁me to eyeTube. Order your Link?", reply_markup=markup)

#=============================================================================================
#About
@bot.message_handler(commands=['About'])
def send_about(message):
    bot.send_photo(message.chat.id, open('logo.jpg', 'rb'),"Introducing ...")
    bot.reply_to(message, '''👁️EyeTubeBot 
▪️As part to contribute to the Societal Evolution into the new Era  full of Technology advancements, the emergence of  Automation in AI has lead us discover innovative ways to solve and change human  repeated processes to a more productive living.

It's a bot, self-employed as a delivery guy🏃‍♂️ collecting all files including; movies,videos and audios from all over the internet(Social Medias) and delivering it into your Computer.

                      
            By ~_AI possibilities Start Up_
       
              _9/2024_''')
    

@bot.message_handler(commands=['Help'])
def open_link_command(message):
    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="✅ Help", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_End_User/Documentation.md")
    button2 = types.InlineKeyboardButton(text="❓ What Can EyeTubeBot Do", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/README.md")

    keyboard.add(button1)
    keyboard.add(button2)
    
    # Send a message with the inline keyboard
    bot.send_message(message.chat.id, '''💁🏻 Explore How to Use EyeTubeB👁t core v1.0.0?\n
                click any!''', reply_markup=keyboard)

                 
#Engineer button should send the user the picture of the developer and picture of his home lab also with a link to his linkedin profile, github profile, whatsapp chat and email address and lastly a qoute from the developer
@bot.message_handler(commands=['Engineer'])
def send_engineer(message):
    bot.reply_to(message, '''@mickekofi
I am an Aspired Artificial Intelligence Engineer in the field of  Systems Automation and Development.

I focus in engineering softwares and systems under the subjects of Data Science and AI in Automation with Python and C++.

Find
✓ LinkedIn : https://www.linkedin.com/in/michael-appiah-9b6919255

✓ GitHub   : https://github.com/Mickekofi

✓ Whatsapp : https://wa.me/233597326320

✓ Mail     : mickekofi6@gmail.com''')



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
        download_url = download_youtube_video(url, quality)
        
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
    bot.polling()

bot_polling()