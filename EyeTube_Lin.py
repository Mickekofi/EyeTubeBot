import yt_dlp
#STAGE 3b
def download_linkedin_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if info_dict:
                if 'entries' in info_dict:
                    # If it's a playlist or multiple entries
                    video_url = info_dict['entries'][0]['url']
                else:
                    # Single video
                    video_url = info_dict['url']
                return video_url
            else:
                return None
    except Exception as e:
        print(f"Error downloading LinkedIn video: {e}")
        return None