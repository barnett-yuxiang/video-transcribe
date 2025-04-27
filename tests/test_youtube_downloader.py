import os
from unittest import mock

import pytest


@pytest.fixture
def fake_info():
    return {
        "id": "testid",
        "formats": [
            {"format_id": "18", "vcodec": "avc1", "height": 360},
            {"format_id": "22", "vcodec": "avc1", "height": 720},
        ],
    }


@mock.patch.dict("sys.modules", {"yt_dlp": mock.Mock()})
def test_download_success(tmp_path, fake_info):
    from youtube_downloader import download

    yt_dlp_mock = mock.MagicMock()
    yt_dlp_mock.YoutubeDL.return_value.__enter__.return_value.extract_info.return_value = (
        fake_info
    )
    yt_dlp_mock.YoutubeDL.return_value.__enter__.return_value.download.return_value = (
        None
    )
    sys_modules = {"yt_dlp": yt_dlp_mock}
    with mock.patch.dict("sys.modules", sys_modules):
        output = download("https://youtu.be/testid", str(tmp_path))
        assert output == os.path.join(str(tmp_path), "testid.mp4")


@mock.patch.dict("sys.modules", {"yt_dlp": mock.Mock()})
def test_download_no_360p(tmp_path, fake_info):
    from youtube_downloader import download

    fake_info_no_360p = {
        "id": "testid",
        "formats": [
            {"format_id": "22", "vcodec": "avc1", "height": 720},
        ],
    }
    yt_dlp_mock = mock.MagicMock()
    yt_dlp_mock.YoutubeDL.return_value.__enter__.return_value.extract_info.return_value = (
        fake_info_no_360p
    )
    sys_modules = {"yt_dlp": yt_dlp_mock}
    with mock.patch.dict("sys.modules", sys_modules):
        with pytest.raises(Exception):
            download("https://youtu.be/testid", str(tmp_path))


@mock.patch.dict("sys.modules", {"yt_dlp": mock.Mock()})
def test_download_already_exists(tmp_path, fake_info):
    from youtube_downloader import download

    yt_dlp_mock = mock.MagicMock()
    yt_dlp_mock.YoutubeDL.return_value.__enter__.return_value.extract_info.return_value = (
        fake_info
    )
    sys_modules = {"yt_dlp": yt_dlp_mock}
    output_path = os.path.join(str(tmp_path), "testid.mp4")
    with open(output_path, "w") as f:
        f.write("dummy")
    with mock.patch.dict("sys.modules", sys_modules):
        output = download("https://youtu.be/testid", str(tmp_path))
        assert output == output_path
