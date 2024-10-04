import yt_dlp
#STAGE 3a
def extract_linkedin_audio_link(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
        'quiet': True,  # Reduce verbosity
        'outtmpl': '%(title)s.%(ext)s',  # Use title for file naming
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)

            # Fetch all available formats and ensure we're handling cases where 'acodec' isn't directly available
            audio_formats = [f for f in info_dict['formats'] if f.get('acodec') and f['acodec'] != 'none']
            if not audio_formats:
                # If no audio formats are found, try to find any format with audio
                audio_formats = [f for f in info_dict['formats'] if f.get('vcodec') == 'none']
            
            if audio_formats:
                audio_url = audio_formats[0]['url']  # Get the first available audio format
                audio_title = info_dict.get('title', 'audio') + ".mp3"
                return audio_url, audio_title  # Return both the URL and title
            else:
                print("No audio formats found. Available formats:")
                for f in info_dict['formats']:
                    print(f"Format ID: {f['format_id']}, Acodec: {f.get('acodec')}, Vcodec: {f.get('vcodec')}")
                return None, None
    except yt_dlp.utils.DownloadError as e:
        print(f"Error extracting audio: {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None, None

