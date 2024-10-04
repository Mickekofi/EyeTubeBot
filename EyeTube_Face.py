import yt_dlp
import logging

#STAGE 3b
#Funtion that fetches and downloads the Video from Facebook
def download_facebook_video(url):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'outtmpl': '%(title)s - %(uploader)s - %(upload_date)s.%(ext)s',
        'quiet': True,
        'extract_flat': 'in_playlist',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        if 'entries' in info_dict:
            video_format = info_dict['entries'][0]
        else:
            video_format = info_dict

        download_url = video_format.get('url')
        if not download_url:
            raise ValueError("Could not extract video URL.")
        
        return download_url