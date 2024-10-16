import yt_dlp
import logging

def download_youtube_video(url, quality='best'):
    try:
        # Define options for yt_dlp
        ydl_opts = {
            'format': f'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if quality == 'best' else 'worst',
            'outtmpl': '%(title)s - %(uploader)s - %(upload_date)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,  # Suppresses output to speed up processing
        }

        # Start the yt_dlp extraction
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            formats = info_dict.get('formats', [])

            # Log available formats for debugging

            # Find video format (with or without audio)
            video_format = None
            audio_format = None

            # Filter video formats with valid height
            video_formats = [f for f in formats if f.get('vcodec') != 'none' and f.get('height') is not None]
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('abr') is not None]

            # Get the best video format based on quality
            if quality == 'best':
                video_format = max(video_formats, key=lambda f: f.get('height', 0), default=None)
                audio_format = max(audio_formats, key=lambda f: f.get('abr', 0), default=None)
            else:
                video_format = min(video_formats, key=lambda f: f.get('height', 0), default=None)
                audio_format = min(audio_formats, key=lambda f: f.get('abr', 0), default=None)

            if video_format:
                video_url = video_format['url']
            else:
                return None
    
            if audio_format:
                audio_url = audio_format['url']
                return {"video :": video_url, "audio_url":"Add '-a' to the link for only audio" } # I have replaced "audio_url" variable with a message to add '-a' to the link for only audio
            else:
                logging.warning("No suitable audio format found.")
                return {"video_url": video_url, "audio_url": None}

    except yt_dlp.utils.DownloadError as e:
        logging.error(f"Download error: {e}")
        return None
    except yt_dlp.utils.ExtractorError as e:
        logging.error(f"Extractor error: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return None
