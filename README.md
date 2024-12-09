# Video to Audio and Subtitles Processor

This project processes video files to extract audio and generate subtitles using the Whisper model.

## Features

- Extracts audio from video files and saves it as WAV files.
- Generates subtitles from the extracted audio.
- Optionally includes timestamps in the subtitles.

## Requirements

- Python 3.6+
- ffmpeg
- whisper
- argparse (part of Python standard library)

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
    pip install -r requirements.txt
    ```

4. Ensure `ffmpeg` is installed and available in your PATH.

## Usage

1. Place your video files (e.g., `example.mp4`) in the `files` directory.

2. Run the script:
    ```sh
    python main.py --timestamps
    ```

    The `--timestamps` flag is optional. If provided, the generated subtitles will include timestamps.

3. The extracted audio and generated subtitles will be saved in the [files](http://_vscodecontentref_/5) directory.

## License

This project is licensed under the MIT License.
