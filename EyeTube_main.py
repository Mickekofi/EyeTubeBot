import telebot
import yt_dlp
import time
import re
from EyeTube_you_a import extract_youtube_audio_link
from EyeTube_you_a import download_youtube_video
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

# Configure logging
logging.basicConfig(level=logging.INFO)


TOKEN = ''
bot = telebot.TeleBot(TOKEN)

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

#make it support this facebook link https://www.facebook.com/share/v/V36zS2gWo4ezB4Rj/?mibextid=
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
#Make the bot to send a welcome message to the user when the user starts the bot

# A list to store user chat IDs
user_chat_ids = set()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Add the user's chat ID to the set
    user_chat_ids.add(message.chat.id)
    save_chat_ids()  # Save chat IDs whenever a new user starts the bot
    
    # Creating buttons
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/Help')
    itembtn2 = telebot.types.KeyboardButton('/About')
    itembtn3 = telebot.types.KeyboardButton('/Engineer')
    itembtn4 = telebot.types.KeyboardButton('/Donate')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.reply_to(message, "Welc👁me to eyeTube. Order your Link?", reply_markup=markup)

#=============================================================================================
# Function to broadcast new feature/fix messages
def broadcast_fix_message(fix_message):
    for chat_id in user_chat_ids:
        try:
            bot.send_message(chat_id, fix_message)
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")


new_feature_message = "🎉 New feature: You can now download videos from LinkedIn! 🎉\n\nPlease note that this feature is still in beta and may not work for all videos. If you encounter any issues, please let us know by sending a message to the developers using the /Engineer command. Thank you for using EyeTube! 🤖"
# Save chat IDs to a file
def save_chat_ids():
    try:
        with open('chat_ids.txt', 'w') as file:
            for chat_id in user_chat_ids:
                file.write(f"{chat_id}\n")
    except Exception as e:
        print(f"Failed to save chat IDs: {e}")

# Load chat IDs from a file
def load_chat_ids():
    global user_chat_ids
    try:
        with open('chat_ids.txt', 'r') as file:
            user_chat_ids = set(line.strip() for line in file)
    except FileNotFoundError:
        user_chat_ids = set()
    except Exception as e:
        print(f"Failed to load chat IDs: {e}")

# Load chat IDs at startup
load_chat_ids()

# Broadcast the message when the bot starts
broadcast_fix_message(new_feature_message)

#About
@bot.message_handler(commands=['About'])
def send_about(message):
    bot.send_photo(message.chat.id, open('logo.jpg', 'rb'),"Introducing ...")
    bot.reply_to(message, '''👁️EyeTubeBot 
▪️As part to contribute to the Societal Evolution into the new Era  full of Technology advancements, the emergence of  Automation in AI has lead us discover innovative ways to solve and change human  repeated processes to a more productive living.

It's a bot, self-employed as a delivery guy🏃‍♂️ collecting all files including; movies,videos and audios from all over the internet(Social Medias) and delivering it into your Computer.

I present to you EyeTubeBot...

Try Today
t.me/EyeTubeAiBot 
                    
You can also use the following commands:\n\n/About - Learn more about EyeTube\n/Help - Get help on how to use EyeTube\n//Engineer - Contact the developers\n/Donate - Support EyeTube)

                      
            By ~_AI possibilities Start Up_
       
              _9/2024_''')
    

@bot.message_handler(commands=['Help'])
def send_help(message):
    #How to use the bot
    bot.send_animation(message.chat.id, open('help.gif', 'rb'),"🔑")

    bot.reply_to(message, '''
                 I accept links from these various sources in the meantime...🙏🏽

1. YouTube
2. LinkedIn
3. Snapchat
4. Facebook
5. Instagram
6. X(Twitter)
7. others

General
Open the video or movie you want to download from the mentioned Social medias above 🖕🏻...

✓ Tap on Share Button > Copy the link > Send it to me.


VIDEO/MOVIE DOWNLOADING
By Default Video Downloads are Set to HD Quality unless you apply the following commands "at the end of your link before send"

✓ -h    =  This is for the highest Quality of the Video or Movie.

✓ -l     = This is for the lowest Quality of the Video or Movie.

AUDIO/MUSIC Only
To Get the audio or Music only make sure you add -a at the end of the link before send.

✓ -a    = It allows you to extract audio only...

Note: Make sure you edit the name of the downloaded file by adding a " .mp3 " to it before it can open it as music.


Other Issues
You can also use the following commands:\n\n/About - Learn more about EyeTube\n/Help - Get help on how to use EyeTube\n/Engineer - Contact the developers\n/Donate - Support EyeTube)

                 By ~_AI possibilities Start Up_
                                   _9/2024_''')

                 
#Engineer button should send the user the picture of the developer and picture of his home lab also with a link to his linkedin profile, github profile, whatsapp chat and email address and lastly a qoute from the developer
@bot.message_handler(commands=['Engineer'])
def send_engineer(message):
    bot.send_photo(message.chat.id, open('Michael.jpg', 'rb'),"""✓ Keep Moving Forward...""")
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
#Make the bot to handle the user's message and check if the user's message is a valid link and then send the user a message to wait while the bot is processing the link using the created handle platform function
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
            return  # Exit the function after handling audio download
        
        # Set default quality
        quality = 'best'
        
        # Check for quality options in the URL
        if '-l' in url:
            quality = 'worst'
            url = url.replace('-l', '').strip()
        elif '-h' in url:
            quality = 'best'  # This line is actually redundant as quality is already set to 'best'

        # Notify the user that the download is in progress
        bot.reply_to(message, "Generating YouTube video download link. Please wait...")
        
        # Call the download function
        download_url = download_youtube_video(url, quality)
        
        # Check the download URL and respond accordingly
        if download_url:
            bot.reply_to(message, f"Here is your download link: {download_url}\n\nPlease note: This link will use your own internet data to download the file.")
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
                bot.reply_to(message, f"Here is your download link: {download_url}\n\nPlease note: This link will use your own internet data to download the file.")
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
                bot.reply_to(message, f"Here is your download link: {download_url}\n\nPlease note: This link will use your own internet data to download the file.")
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
            bot.reply_to(message, f"Here is your download link: {video_url}\n\nPlease note: This link will use your own internet data to download the file.")
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
                bot.reply_to(message, f"Here is your download link: {video_url}\n\nPlease note: This link will use your own internet data to download the file.")
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
            bot.reply_to(message, f"Here is your download link: {video_url}\n\nPlease note: This link will use your own internet data to download the file.")
        except Exception as e:
            bot.reply_to(message, f"Failed to download video: {e}")





#STAGE 4a
#==============================================================================
#This is where the send_audio_link function is defined to send the user the download link for the audio based on the hard work of the Audio extraction functions called the "extract_platform_audio_link" function which are in their independent files

def send_audiomack_audio(message, url):
    audio_url = extract_audiomack_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your AudioMack download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")
    else:
        bot.reply_to(message, "Failed to extract the audio download link.")


def send_youtube_audio(message, url):
    audio_url = extract_youtube_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your YouTube download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")


def send_instagram_audio(message, url):
    audio_url = extract_instagram_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Instagram download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")

def send_facebook_audio(message, url):
    audio_url = extract_facebook_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Facebook download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")



def send_twitter_audio(message, url):
    audio_url = extract_twitter_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Twitter download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")


def send_linkedin_audio(message, url):
    audio_url = extract_linkedin_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your LinkedIn download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")

def send_snapchat_audio(message, url):
    audio_url = extract_snapchat_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your Snapchat download link: {audio_url}\n\nPlease note: This link will use your own internet data to download the file.")

#==============================================================================
#This is where the bot is set to keep polling for new messages and retry on failure
@retry_on_failure
def bot_polling():
    bot.polling()

bot_polling()