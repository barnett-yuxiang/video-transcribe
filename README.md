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

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Ensure `ffmpeg` is installed and available in your PATH.

## Usage

1. Place your video files in the `files` directory.

2. Run the script:
    ```sh
    python main.py --timestamps
    ```

    The `--timestamps` flag is optional. If provided, the generated subtitles will include timestamps.

3. The extracted audio and generated subtitles will be saved in the [files](http://_vscodecontentref_/0) directory.

## Code Overview

- [main.py](http://_vscodecontentref_/1): The main script that processes video files.
  - [format_timestamp(seconds)](http://_vscodecontentref_/2): Converts seconds to `hh:mm:ss` format.
  - [extract_audio(video_path, output_path)](http://_vscodecontentref_/3): Extracts audio from a video file.
  - [transcribe_audio(model, audio_path, include_timestamps)](http://_vscodecontentref_/4): Transcribes audio to subtitles.
  - [process_video(video_path, output_folder, model_name, include_timestamps)](http://_vscodecontentref_/5): Processes a video file to generate audio and subtitles.

## License

This project is licensed under the MIT License.