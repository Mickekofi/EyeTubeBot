import yt_dlp
#Step 3a
def extract_twitter_audio_link(url):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,
        'force_generic_extractor': False  # Ensure yt-dlp tries specific extractors
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            audio_url = next((f['url'] for f in info_dict['formats'] if f.get('acodec') != 'none' and f['ext'] in ['m4a', 'mp3']), None)
            if audio_url:
                return audio_url
            else:
                print("No audio format found.")
                return None
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
