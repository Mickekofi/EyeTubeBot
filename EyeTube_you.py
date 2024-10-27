import yt_dlp
import logging

# Function that fetches and downloads the Video from YouTube
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'outtmpl': '%(title).100B [%(id)s].%(ext)s',  # Limit title length and add video ID
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if 'entries' in info_dict:
            video_format = info_dict['entries'][0]  # For playlists, select the first video
        else:
            video_format = info_dict

        download_url = video_format.get('url')
        if not download_url:
            raise ValueError("Could not extract video URL.")
        
        return download_url