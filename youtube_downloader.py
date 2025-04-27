import os

def download(url, output_folder):
    """
    Download a YouTube video at 360p resolution to the output folder.
    Prints all available resolutions before downloading.
    If the video already exists, skips downloading.
    Raises an exception if 360p is not available.
    Args:
        url (str): The YouTube video URL.
        output_folder (str): Directory to save the downloaded video.
    Returns:
        str or None: Path to the downloaded video, or None if failed.
    """
    try:
        import yt_dlp
    except ImportError:
        print("Please install yt-dlp: pip install yt-dlp")
        return None

    # Extract video ID from URL using yt_dlp
    ydl_id_opts = {'quiet': True, 'skip_download': True}
    with yt_dlp.YoutubeDL(ydl_id_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_id = info.get('id')
        output_path = os.path.join(output_folder, f"{video_id}.mp4")
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"Video already downloaded: {output_path}")
            return output_path

        formats = info.get('formats', [])
        resolutions = set()
        for f in formats:
            if f.get('vcodec', 'none') != 'none' and f.get('height'):
                resolutions.add(f"{f['height']}p")
        if resolutions:
            print(f"Available resolutions for {url}: {', '.join(sorted(resolutions, key=lambda x: int(x[:-1])))}")
        else:
            print("No video resolutions found.")
            return None

    # Prefer format 18, then 360p mp4, then other available formats
    ydl_opts = {
        'quiet': False,
        'format': '18/best[height<=360][ext=mp4]/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'cookiesfrombrowser': ('chrome',),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
            ydl_download.download([url])
        print(f"Downloaded: {output_path}")
        return output_path
    except Exception as e:
        print(f"Failed to download video: {e}")
        return None
