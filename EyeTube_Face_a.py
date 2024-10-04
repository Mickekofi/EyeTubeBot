import yt_dlp

#STAGE 3a
# Function to extract audio link from Facebook video
def extract_facebook_audio_link(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s - %(uploader)s - %(upload_date)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'extractaudio': True,  # Ensure only audio is extracted
        'audioformat': 'mp3',  # Ensure the audio format is mp3
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        audio_url = info_dict.get('url', None)
    
    return audio_url

