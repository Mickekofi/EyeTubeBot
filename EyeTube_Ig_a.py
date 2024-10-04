import yt_dlp
#STAGE 3a
#Function to extract audio link from Instagram video
def extract_instagram_audio_link(url):
    ydl_opts = {
        'format': 'bestaudio/best',  # Get the best available audio-only format
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Extract info only
        formats = info_dict.get('formats', [])
        
        # Find and return the first available .m4a format
        audio_url = next(
            (f['url'] for f in formats if f.get('ext') == 'm4a'), None
        )
    
    return audio_url

