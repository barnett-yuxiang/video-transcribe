# Video to Audio and Subtitles Processor

This project processes video files or YouTube links to extract audio and generate subtitles using the Whisper model.

## Features

- Extracts audio from video files (e.g., `.mp4`, `.mov`) and saves as **WAV** files.
- Downloads YouTube videos at 360p (if a YouTube URL is provided).
- Generates subtitles from the extracted audio using OpenAI Whisper (supports Chinese and other languages).
- Optionally includes timestamps in the subtitles.
- Simple command-line interface with flexible options.

## Requirements

- Python 3.10+
- ffmpeg
- openai-whisper
- yt-dlp
- argparse (Python standard library)
- Ensure `ffmpeg` is installed and available in your PATH.
- **For YouTube downloads**: You must be logged into YouTube in Chrome, Safari, or Firefox browser to bypass bot detection.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    make install-dev
    ```

## Usage

You can process either a local video file or a YouTube URL.

### Process a local video file

1. Place your video files (e.g., `example.mp4`) in the `files` directory (or provide the full path).

2. Run the script:
    ```sh
    python main.py files/example.mp4 --timestamps
    ```

### Process a YouTube video

**⚠️ Important: Before downloading YouTube videos**

To avoid YouTube's bot detection, you need to:

1. Open **Chrome, Safari, or Firefox** browser
2. Visit `youtube.com` and log in with your account
3. Watch a few videos to ensure cookies are saved
4. Keep the browser installed (cookies will be automatically used)

The script will automatically extract cookies from your browser to authenticate the download.

**Download and process:**

1. Run the script with a YouTube URL:
    ```sh
    python main.py "https://www.youtube.com/watch?v=xxxxxxx" --timestamps
    ```

    The video will be downloaded to the `files` directory and processed automatically.

### Command-line options

- `uri` (positional): Local file path or YouTube URL.
- `-t`, `--timestamps`: Include timestamps in the subtitles.
- `-d`, `--download-only`: Only download the YouTube video to the `files` directory, do not process.

### Output

- Extracted audio: `{video_id or filename}.wav` in the `files` directory.
- Subtitles: `{video_id or filename}.txt` in the `files` directory.

## Example

```sh
python main.py "https://www.youtube.com/watch?v=xxxxxxx" --timestamps
```

## Troubleshooting

### YouTube download fails with "Sign in to confirm you're not a bot"

This happens when YouTube's bot detection blocks the download. To fix:

1. **Ensure browser login** (most common solution):
   - Open Chrome, Safari, or Firefox
   - Go to `youtube.com` and log in
   - Browse/watch a few videos to save cookies
   - Run the script again

2. **Check browser availability**:
   - The script tries Chrome → Safari → Firefox in order
   - Make sure at least one is installed and you're logged in
   - You'll see a message: "Using cookies from [Browser] browser"

3. **If still failing**:
   - Try opening an incognito/private window and ensure you can watch videos
   - Clear your browser cache and log in again
   - Try a different browser

The script automatically extracts and uses browser cookies to authenticate your downloads.

## License

This project is licensed under the MIT License.
