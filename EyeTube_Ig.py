import yt_dlp
#STAGE 3b
#Function to fectch the download URL of Instagram content
def download_instagram_content(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            download_url = info_dict['url']
            return download_url
    except Exception as e:
        print(f"Error: {e}")
        return None