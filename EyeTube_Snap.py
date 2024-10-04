import yt_dlp
#STEP 3b
# Function to extract the video URL
def download_snapchat_video(url):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
        'skip_download': True  # Do not download the video
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            if 'entries' in info_dict:
                video_info = info_dict['entries'][0]
            else:
                video_info = info_dict
            
            video_url = video_info.get('url')
            title = video_info.get('title', 'video')
            return video_url
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
