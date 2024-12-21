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
import pw
import support
import subprocess
import requests
from bs4 import BeautifulSoup
import logging
import whois

from update_checker import UpdateChecker

logging.basicConfig(level=logging.INFO)
pw.auto()
print("\033[93mLets start EyeTubeBot 2 0 1...\n\033[0m")
support.check_support()
admin = input("\033[92mPlease enter your name 👉 : \033[0m")
TOKEN = input("\n\033[92mPlease enter your Telegram API token 👉 : \033[0m")

if not TOKEN:
    print("\033[91m❓You provided No API token.\n\n Shuting down/Exiting...\033[0m")
    exit(1)

try:
    bot = telebot.TeleBot(TOKEN)
    print("\033[92mBot initialized successfully!\033[0m")
    
    bot_info = bot.get_me()
    print(f"\033[92mBot Username: {bot_info.username}\033[0m")
    print("\033[92mReady to receive commands.\033[0m")
    
except Exception as e:
    print(f"\033[91mError: Failed to initialize bot. {e}\033[0m")
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
            update_button = InlineKeyboardButton("🎁 𝗖𝗵𝗲𝗰𝗸 𝗪𝗵𝗮𝘁 𝗶𝘀 𝗡𝗲𝘄𝗹𝘆 𝗣𝗮𝗰𝗸𝗲𝗱 𝗳𝗼𝗿 𝘆𝗼𝘂", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/update.md")
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

def is_valid_url(url):
    # This regex will match a wide variety of valid URLs including subdomains, paths, and query strings
    url_regex = re.compile(
        r'^(https?://)?'  # Optional scheme (http or https)
        r'([a-zA-Z0-9-]+\.)+'  # Subdomains (optional) and main domain
        r'[a-zA-Z]{2,}'  # Top-level domain (e.g., .com, .org, etc.)
        r'(:[0-9]{1,5})?'  # Optional port number
        r'(/[^\s]*)?$'  # Optional path and query string
    )
    return bool(url_regex.match(url))





# WELCOME START
#==============================================================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/Help')
    itembtn2 = telebot.types.KeyboardButton('/Engineer')
    itembtn3 = telebot.types.KeyboardButton('/check_update')
    itembtn4 = telebot.types.KeyboardButton('/update')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.reply_to(message, f"🕹 {bot_info.username} is Operated by {admin}.\n\n𝙋𝙖𝙨𝙩𝙚 𝙮𝙤𝙪𝙧 𝙎𝙤𝙘𝙞𝙖𝙡 𝙈𝙚𝙙𝙞𝙖 🎬 𝙑𝙞𝙙𝙚𝙤 𝙇𝙞𝙣𝙠  𝙝𝙚𝙧𝙚 𝙤𝙧 𝙖𝙣𝙮 𝙬𝙚𝙗 𝙡𝙞𝙣𝙠 📎?", reply_markup=markup)

#============================================================================================
#About
@bot.message_handler(commands=['Help'])
def open_about_command(message):
    keyboard = types.InlineKeyboardMarkup()

    button6 = types.InlineKeyboardButton(text="Visit Our Page", url="https://github.com/Mickekofi/EyeTubeBot")
    button1 = types.InlineKeyboardButton(text="📚 Learn about EyeTubeBot Version(2.0.1)", url="https://github.com/Mickekofi/EyeTubeBot/blob/master/Documentation_For_Dev/Documentation.md")
    button4 = types.InlineKeyboardButton(text="👥 Who are We", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_End_User_/Who_are_we.md")
    button5 = types.InlineKeyboardButton(text="What is in for this Update", url="https://github.com/Mickekofi/EyeTubeBot/tree/master/Documentation_For_Dev/update.md")
    
    keyboard.add(button6)  
    keyboard.add(button1)
    keyboard.add(button4)  
    keyboard.add(button5)

    bot.send_message(message.chat.id, "About Info", reply_markup=keyboard)

    bot.send_message(message.chat.id,'''❓𝐒𝐮𝐠𝐠𝐞𝐬𝐭 𝐚𝐧 𝐈𝐬𝐬𝐮𝐞 𝐚 𝐁𝐮𝐠 𝐨𝐫 𝐚 𝐅𝐞𝐚𝐭𝐮𝐫𝐞 𝐑𝐞𝐪𝐮𝐞𝐬𝐭?📬;
    
    𝙍𝙚𝙥𝙤𝙧𝙩 𝙩𝙤 𝙂𝙞𝙩𝙝𝙪𝙗 𝙤𝙧 𝐜𝐨𝐩𝐲 𝐚𝐧𝐝 𝐩𝐚𝐬𝐭𝐞 𝙩𝙝𝙚 𝙎𝙩𝙧𝙞𝙣𝙜𝙨 𝙗𝙚𝙡𝙤𝙬 𝐢𝐧 𝐲𝐨𝐮𝐫 𝐛𝐫𝐨𝐰𝐬𝐞𝐫 
                     👇👇👇''')
    bot.send_message(message.chat.id, f'''mailto:eyetubebot@gmail.com?subject=📬ID_{message.from_user.id}%20[Issue]%20Report%20&body=(🖇Please_Attach_your_Issue_screenshot)%0A%0A-[Country]:%0A%0A%0A%0A-%5BPlease%20describe%20your%20Issue%20here%5D%20:
                     ''')
    

    
@bot.message_handler(commands=['Engineer'])
def send_engineer(message):
    bot.send_photo(message.chat.id, open('Michael.jpg', 'rb'), caption="💬 \"🅰🅽🆈🅾🅽🅴 🅲🅰🅽 🅲🅾🅾🅺\" - 𝗠𝗶𝗰𝗵𝗮𝗲𝗹 𝗔𝗽𝗽𝗶𝗮𝗵")

    bot.reply_to(message, """
    
𝐘𝐞𝐥𝐥𝐨 , 𝐈'𝐦 𝐌𝐢𝐜𝐡𝐚𝐞𝐥 𝐀𝐩𝐩𝐢𝐚𝐡, 𝐚𝐧 𝐚𝐬𝐩𝐢𝐫𝐢𝐧𝐠 𝐀𝐫𝐭𝐢𝐟𝐢𝐜𝐢𝐚𝐥 𝐈𝐧𝐭𝐞𝐥𝐥𝐢𝐠𝐞𝐧𝐜𝐞 𝐄𝐧𝐠𝐢𝐧𝐞𝐞𝐫 𝐚𝐧𝐝 𝐭𝐡𝐞 𝐥𝐞𝐚𝐝𝐞𝐫 𝐨𝐟 𝐏𝐨𝐬𝐬𝐢𝐛𝐢𝐥𝐢𝐭𝐲 𝐀𝐢 𝐚𝐧𝐝 𝐂𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐚 𝐒𝐭𝐮𝐝𝐞𝐧𝐭 𝐨𝐟 𝐭𝐡𝐞 𝐔𝐧𝐢𝐯𝐞𝐫𝐬𝐢𝐭𝐲 𝐨𝐟 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧, 𝐖𝐢𝐧𝐧𝐞𝐛𝐚.
    
    𝐈 𝐬𝐩𝐞𝐜𝐢𝐚𝐥𝐢𝐳𝐞 𝐢𝐧 𝐁𝐮𝐢𝐥𝐝𝐢𝐧𝐠 𝐀𝐢 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐞𝐝 𝐂𝐡𝐚𝐭𝐁𝐨𝐭𝐬, 𝐒𝐲𝐬𝐭𝐞𝐦𝐬 𝐀𝐮𝐭𝐨𝐦𝐚𝐭𝐢𝐨𝐧 𝐚𝐧𝐝 𝐒𝐨𝐟𝐭𝐰𝐚𝐫𝐞 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐦𝐞𝐧𝐭 𝐮𝐬𝐢𝐧𝐠 𝐏𝐲𝐭𝐡𝐨𝐧 𝐚𝐧𝐝 𝐂++.

    𝐂𝐨𝐧𝐧𝐞𝐜𝐭 𝐰𝐢𝐭𝐡 𝐦𝐞:  
               
    • 𝙇𝙞𝙣𝙠𝙚𝙙𝙄𝙣: [𝙈𝙞𝙘𝙝𝙖𝙚𝙡 𝘼𝙥𝙥𝙞𝙖𝙝]( https://www.linkedin.com/in/michael-appiah-9b6919255 ) 💼
                 
   
    • 𝙂𝙞𝙩𝙃𝙪𝙗: [𝙈𝙞𝙘𝙠𝙚𝙠𝙤𝙛𝙞] ( https://github.com/Mickekofi ) 🧑‍💻
    
    
                 
            ©️ Possibility AI `24
                                  
    """)








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
    elif is_valid_url(url):
        process_link(message, url)
    else:
        bot.reply_to(message, "Sorry, this link is not valid😢")
        #open the start command automatically withot the user typing it or clicking on the start button
        send_welcome(message)
    











#STAGE 4b
#==============================================================================
#This is Where the platform handle functions is defined with two conditions or Roads and checks the string link again if the user wants to download the audio(-a) or video(default) of the link. It then sends the users choice on the right path to the respective "send_audio_link" or "send_video_link" function for further processing and extraction of the download link
# Handle the AudioMack URL
# Handle AudioMack URL
def handle_audiomack_url(message, url):
    bot.reply_to(message, "AudioMack only supports audio downloads. Please wait while I fetch the link...")
    try:
        send_audiomack_audio(message, url)
    except Exception as e:
        bot.reply_to(message, f"Error: {e}. Retrying in 5 seconds...")
        logging.error(f"Error in handling AudioMack URL: {e}")

# Handle YouTube URL
def handle_youtube_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "📺 Fetching YouTube video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return

        # Determine audio or video download request
        if ' -a' in url:
            bot.reply_to(message, "🎤 Generating YouTube audio download link...")
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
        cookies_file = 'you1cookies.txt'  # Define the path to your cookies file
        download_url = download_youtube_video(url)
        
        # Check the download URL and respond accordingly
        if download_url:
            bot.reply_to(message, f"✅ Here is your download link: {download_url}\n\n🚓check : [ /status ]")
        else:
            send_error_message(message, "Youtube")

    except Exception as e:
        logging.error(f"Error in handling YouTube URL: {e}")
        send_error_message(message, "Youtube")
        # Optional: You could implement a retry mechanism here if desired


def handle_instagram_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "🧲 Fetching Instagram video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return
        
        if ' -a' in url:
            bot.reply_to(message, "🎵 Generating Instagram audio download link...")
            send_instagram_audio(message, url.replace(' -a', '').strip())
            return
        
        bot.reply_to(message, "📺 Downloading Instagram video. Please wait...")
        download_url = download_instagram_content(url.strip())
        
        if download_url:
            bot.reply_to(message, f"✅ Here is your download link: {download_url}\n\n🚓 Check: [ /status ]")
        else:
            send_error_message(message, "Instagram")
    
    except Exception as e:
        logging.error(f"Error handling Instagram URL: {e}")
        send_error_message(message, "Instagram")


def handle_twitter_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "🧲 Fetching Twitter video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return

        if ' -a' in url:
            bot.reply_to(message, "🎤 Generating Twitter audio download link...")
            send_twitter_audio(message, url.replace(' -a', '').strip())
            return

        bot.reply_to(message, "📺 Generating Twitter video download link. Please wait...")
        download_url = download_twitter_video(url.strip())
        
        if download_url:
            bot.reply_to(message, f"✅ Here is your download link: {download_url}\n\n🚓 Check: [ /status ]")
        else:
            send_error_message(message, "Twitter")
    
    except Exception as e:
        logging.error(f"Error handling Twitter URL: {e}")
        send_error_message(message, "Twitter")


def handle_facebook_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "🧲 Fetching Facebook video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return

        if ' -a' in url:
            bot.reply_to(message, "🎤 Generating Facebook audio download link...")
            send_facebook_audio(message, url.replace(' -a', '').strip())
            return

        bot.reply_to(message, "📺 Downloading Facebook video. Please wait...")
        video_url = download_facebook_video(url.strip())
        
        if video_url:
            bot.reply_to(message, f"✅ Here is your download link: {video_url}\n\n🚓 Check: [ /status ]")
        else:
            send_error_message(message, "Facebook")
    
    except Exception as e:
        logging.error(f"Error handling Facebook URL: {e}")
        send_error_message(message, "Facebook")


def handle_linkedin_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "🧲 Fetching LinkedIn video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return

        if ' -a' in url:
            bot.reply_to(message, "🎤 Generating LinkedIn audio download link...")
            send_linkedin_audio(message, url.replace(' -a', '').strip())
            return

        bot.reply_to(message, "📺 Downloading LinkedIn video. Please wait...")
        video_url = download_linkedin_video(url.strip())
        
        if video_url:
            bot.reply_to(message, f"✅ Here is your download link: {video_url}\n\n🚓 Check: [ /status ]")
        else:
            send_error_message(message, "LinkedIn")
    
    except Exception as e:
        logging.error(f"Error handling LinkedIn URL: {e}")
        send_error_message(message, "LinkedIn")


def handle_snapchat_url(message, url):
    try:
        if ' -info' in url:
            bot.reply_to(message, "🧲 Fetching Snapchat video information. Please wait...")
            process_media(message, url.replace('-info', '').strip())
            return

        if ' -a' in url:
            bot.reply_to(message, "🎤 Generating Snapchat audio download link...")
            send_snapchat_audio(message, url.replace(' -a', '').strip())
            return

        bot.reply_to(message, "📺 Downloading Snapchat video. Please wait...")
        video_url = download_snapchat_video(url.strip())
        
        if video_url:
            bot.reply_to(message, f"✅ Here is your download link: {video_url}\n\n🚓 Check: [ /status ]")
        else:
            send_error_message(message, "Snapchat")
    
    except Exception as e:
        logging.error(f"Error handling Snapchat URL: {e}")
        send_error_message(message, "Snapchat")


def send_error_message(message, platform):
    """Send a generic error message with platform-specific details."""
    # First block of the message
    error_message = (
        f"❓ ERROR: Unable to process your {platform} request.\n\n"
        "𝙍𝙚𝙥𝙤𝙧𝙩 𝙩𝙝𝙞𝙨 𝙄𝙨𝙨𝙪𝙚 𝙤𝙣 𝙂𝙞𝙩𝙃𝙪𝙗 𝙤𝙧 𝐜𝐨𝐩𝐲 𝐚𝐧𝐝 𝐩𝐚𝐬𝐭𝐞 𝙩𝙝𝙚 𝙎𝙩𝙧𝙞𝙣𝙜𝙨 𝙗𝙚𝙡𝙤𝙬 𝙞𝙣 𝙮𝙤𝙪𝙧 𝙗𝙧𝙤𝙬𝙨𝙚𝙧\n    👇 👇 👇.\n\n"
    )
    
    bot.send_message(message.chat.id, error_message)

    # Second block of the message
    email_template = (
        f"mailto:eyetubebot@gmail.com?subject=📬ID_{message.from_user.id}%20[Issue]%20Report%20&"
        "body=(🖇Please_Attach_your_Issue_screenshot)%0A%0A-[Country]:%0A%0A%0A%0A-"
        "[Please describe your Issue here]:"
    )

    bot.send_message(message.chat.id, email_template)



#STAGE 4a
#==============================================================================
#This is where the send_audio_link function is defined to send the user the download link for the audio based on the hard work of the Audio extraction functions called the "extract_platform_audio_link" function which are in their independent files

def send_audiomack_audio(message, url):
    audio_url = extract_audiomack_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your AudioMack download link: {audio_url}\n\n")
    else:
        send_error_message(message, "AudioMack")

def send_youtube_audio(message, url):
    audio_url = extract_youtube_audio_link(url)
    if audio_url:
        bot.reply_to(message, f"Here is your YouTube download link: {audio_url}\n\n.")
    else:
        send_error_message(message, "YouTube")

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





#WEBSITE INFO
#==============================================================================
# Process Links Based on Platform
def process_media(message, url):
    if is_valid_url(url):
        try:
            if "youtube.com" in url or "youtu.be" in url:
                metadata = fetch_youtube_metadata(url)
                platform = "YouTube 🎥"
            elif "twitter.com" in url:
                metadata = fetch_twitter_metadata(url)
                platform = "Twitter 🐦"
            elif "facebook.com" in url:
                metadata = fetch_facebook_metadata(url)
                platform = "Facebook 📘"
            elif "instagram.com" in url:
                metadata = fetch_instagram_metadata(url)
                platform = "Instagram 📸"
            elif "linkedin.com" in url:
                metadata = fetch_linkedin_metadata(url)
                platform = "LinkedIn 💼"
            else:
                bot.reply_to(message, "Platform not supported 😢")
                return

            # Send metadata to user with emojis
            bot.reply_to(message, (
                f"✅ Platform: {platform}\n\n"
                f"🌐 Title: {metadata.get('title', 'No title found')}\n\n"
                f"📝 Description: {metadata.get('description', 'No description found')}\n\n"
                f"🔗 URL: {metadata.get('url', 'No URL found')}\n\n"
                f"📸 Image/Thumbnail: {metadata.get('image', metadata.get('thumbnail', 'No image found'))}\n\n\n🚓check : [ /status ]"
            ))
        except Exception as e:
            bot.reply_to(message, f"Oops! Something went wrong while fetching the data 😓\nError: {str(e)}")
    else:
        bot.reply_to(message, "Invalid URL. Please check the link and try again. 🚨")


# YouTube Metadata Scraper
def fetch_youtube_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'title': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else 'No title found',
            'description': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else 'No description found',
            'thumbnail': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'No thumbnail found',
            'url': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else 'No URL found'
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}


# Twitter Metadata Scraper
def fetch_twitter_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'title': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else 'No title found',
            'description': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else 'No description found',
            'image': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'No image found',
            'url': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else 'No URL found'
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}


# Facebook Metadata Scraper
def fetch_facebook_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'title': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else 'No title found',
            'description': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else 'No description found',
            'image': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'No image found',
            'url': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else 'No URL found'
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}


# Instagram Metadata Scraper
def fetch_instagram_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'title': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else 'No title found',
            'description': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else 'No description found',
            'image': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'No image found',
            'url': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else 'No URL found'
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}


# LinkedIn Metadata Scraper
def fetch_linkedin_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        metadata = {
            'title': soup.find('meta', attrs={'property': 'og:title'})['content'] if soup.find('meta', attrs={'property': 'og:title'}) else 'No title found',
            'description': soup.find('meta', attrs={'property': 'og:description'})['content'] if soup.find('meta', attrs={'property': 'og:description'}) else 'No description found',
            'image': soup.find('meta', attrs={'property': 'og:image'})['content'] if soup.find('meta', attrs={'property': 'og:image'}) else 'No image found',
            'url': soup.find('meta', attrs={'property': 'og:url'})['content'] if soup.find('meta', attrs={'property': 'og:url'}) else 'No URL found'
        }
        return metadata
    except Exception as e:
        return {"error": str(e)}


# Bot Message Handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text.strip()  # Expect a URL in the message
    process_media(message, url)  # Process the URL and fetch metadata




#WEBSITE INFO FOR ANY LINK
#==============================================================================
def extract_metadata(url):
    try:
        # Fetch the main URL
        response = requests.get(url)
        response.raise_for_status()  # Handle bad responses (like 404)

        # HTTP Status Code
        http_status = response.status_code

        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract title
        title = soup.title.string if soup.title else 'No title found 🧐'

        # Extract description
        description = soup.find('meta', attrs={'name': 'description'})
        description_content = description['content'] if description else 'No description found 🤷‍♂️'

        # Extract canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        canonical_url = canonical['href'] if canonical else 'No canonical URL found 🔗'

        # Extract author
        owner = soup.find('meta', attrs={'name': 'author'})
        owner_content = owner['content'] if owner else 'No author information found 🤔'

        # Extract keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        keywords_content = keywords['content'] if keywords else 'No keywords found 🔑'

        # Extract OpenGraph metadata (if available)
        og_title = soup.find('meta', attrs={'property': 'og:title'})
        og_title_content = og_title['content'] if og_title else 'No OpenGraph title found 📱'

        # Check for basic safety (simple heuristic)
        is_safe = "✅ Safe and sound!" if "phishing" not in response.text.lower() else "⚠️ Potentially unsafe website!"

        # WHOIS information
        whois_info = whois.whois(url)
        creation_date = whois_info.creation_date if whois_info.creation_date else 'No creation date found 📅'

        # Check for robots.txt file (gracefully handle 404)
        robots_url = url.rstrip('/') + "/robots.txt"
        try:
            robots_response = requests.get(robots_url)
            if robots_response.status_code == 200:
                robots_content = robots_response.text
            else:
                robots_content = 'No robots.txt file found 🤖'
        except requests.exceptions.HTTPError:
            robots_content = 'No robots.txt file found 🤖'

        # Gather social media links (optional)
        social_links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if "facebook.com" in href:
                social_links.append("📘 Facebook")
            elif "twitter.com" in href:
                social_links.append("🐦 Twitter")
            elif "linkedin.com" in href:
                social_links.append("🔗 LinkedIn")

        social_links = social_links if social_links else ['No social media links found 🚫']

        # Return all extracted information with emojis for fun output
        return {
            'title': title,
            'description': description_content,
            'owner': owner_content,
            'canonical_url': canonical_url,
            'keywords': keywords_content,
            'http_status': f"HTTP Status: {http_status} 🖥️",
            'is_safe': is_safe,
            'creation_date': creation_date,
            'robots_content': robots_content,
            'open_graph_title': og_title_content,
            'social_links': ', '.join(social_links)
        }

    # Handle errors for specific HTTP issues
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"\nno data: We managed to 🔑get this for you 🛑: {http_err}"}

    # Handle request errors
    except requests.exceptions.RequestException as req_err:
        return {"error": f"Request error occurred ❗: {req_err}"}

    # Handle any other exceptions
    except Exception as e:
        return {"error": f"Unexpected error occurred 🤯: {str(e)}"}


# Step 3: Process Links Function
def process_link(message, url):
    try:
        if is_valid_url(url):
            bot.reply_to(message, "🛠️ Digging Information from the provided Site... 🌐")
            metadata = extract_metadata(url)
            # Send metadata to user
            if "error" in metadata:
                bot.reply_to(message, f"⚠️ This page/site is ⛓protected  : {metadata['error']},\n\n please click this👆 link then copy & paste to me")
            else:
                bot.reply_to(message, (
                    f"🎯 Title: {metadata['title']}\n\n"
                    f"📝 Description: {metadata['description']}\n\n"
                    f"👤 Owner: {metadata['owner']}\n\n"
                    f"🔗 Canonical URL: {metadata['canonical_url']}\n\n"
                    f"🔑 Keywords: {metadata['keywords']}\n\n"
                    f"📡 OpenGraph Title: {metadata['open_graph_title']}\n\n"
                    f"🛡️ Safety Status: {metadata['is_safe']}\n\n"
                    f"📅 Creation Date: {metadata['creation_date']}\n\n"
                    f"🤖 robots.txt Content: {metadata['robots_content']}\n\n"
                    f"🌐 Social Media Links: {metadata['social_links']}\n\n"
                    f"🖥️ HTTP Status Code: {metadata['http_status']}\n\n\n🚓check : [ /status ]"
                ))
        else:
            bot.reply_to(message, "❌ Invalid URL. Please check the link and try again.")
    except Exception as e:
        bot.reply_to(message, f"😞 We're sorry, This page/site has an Advanced ⛓protection. We are working 24/7 to break into links like these")






#==============================================================================
@retry_on_failure
def bot_polling():
    bot.polling(none_stop=True, timeout=60)

bot_polling()