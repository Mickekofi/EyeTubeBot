import yt_dlp
import logging
#Step 3b
def download_youtube_video(url, quality):
    try:
        ydl_opts = {
            'format': f'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if quality == 'best' else 'worst',
            'outtmpl': '%(title)s - %(uploader)s - %(upload_date)s.%(ext)s',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            # Debugging format options
            logging.info(f"Available formats: {info_dict['formats']}")
            
            video_format = next((f for f in info_dict['formats'] if f.get('vcodec') != 'none' and f.get('acodec') != 'none'), None)

            if video_format:
                download_url = video_format['url']
                logging.info(f"Generated download URL: {download_url}")
                return download_url
            else:
                logging.error("No suitable format found for download.")
                return None

    except Exception as e:
        logging.error(f"Error downloading YouTube video: {e}")
        return None
