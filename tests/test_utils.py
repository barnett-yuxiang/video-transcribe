import pytest
from utils import is_youtube_url


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://www.youtube.com/watch?v=abc123", True),
        ("http://youtube.com/watch?v=abc123", True),
        ("https://youtu.be/abc123", True),
        ("www.youtube.com/watch?v=abc123", True),
        ("youtu.be/abc123", True),
        ("https://notyoutube.com/watch?v=abc123", False),
        ("https://vimeo.com/123456", False),
        ("randomstring", False),
        ("", False),
    ],
)
def test_is_youtube_url(url, expected):
    assert is_youtube_url(url) == expected
