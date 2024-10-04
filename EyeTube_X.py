import yt_dlp
#Step 3b
def download_twitter_video(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_url = info_dict['url']
            return video_url
    except Exception as e:
        print(f"Error: {e}")
        return None