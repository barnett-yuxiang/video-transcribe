import re

def is_youtube_url(url):
    """
    Check if the given string is a YouTube URL.
    Args:
        url (str): The URI to check.
    Returns:
        bool: True if the URI is a YouTube URL, False otherwise.
    """
    youtube_regex = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/"
    return re.match(youtube_regex, url) is not None
