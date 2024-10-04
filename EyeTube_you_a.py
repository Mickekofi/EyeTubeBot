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

