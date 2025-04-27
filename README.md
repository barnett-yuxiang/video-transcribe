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

## License

This project is licensed under the MIT License.
