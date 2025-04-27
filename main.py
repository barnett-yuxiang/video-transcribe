import os
import ffmpeg
import whisper
from datetime import timedelta
import argparse
from utils import is_youtube_url


def format_timestamp(seconds):
    """
    Convert seconds to hh:mm:ss format.
    Args:
        seconds (float): Time in seconds.
    Returns:
        str: Time formatted as hh:mm:ss.
    """
    td = timedelta(seconds=round(seconds))
    return str(td)


def extract_audio(video_path, output_path):
    """
    Extract audio from a video file and save as a WAV file.
    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path where the audio file will be saved.
    Returns:
        str: Path to the extracted audio file.
    """
    audio_file = os.path.join(
        output_path, f"{os.path.splitext(os.path.basename(video_path))[0]}.wav"
    )
    ffmpeg.input(video_path).output(
        audio_file, format="wav", acodec="pcm_s16le", ac=1, ar="16000"
    ).run(quiet=True)
    return audio_file


def transcribe_audio(audio_path, include_timestamps=False):
    """
    Transcribe an audio file using Whisper.
    Args:
        audio_path (str): Path to the audio file to transcribe.
        include_timestamps (bool): Whether to include timestamps in the output.
    Returns:
        list: List of transcribed lines, optionally with timestamps.
    """
    # Load the model
    model = whisper.load_model("medium")

    # Configure Chinese transcription
    result = model.transcribe(
        audio_path, language="zh", task="transcribe", word_timestamps=True
    )

    segments = result["segments"]
    lines = []

    for segment in segments:
        if include_timestamps:
            # Format and include timestamps in the subtitle line
            start = format_timestamp(segment["start"])
            end = format_timestamp(segment["end"])
            text = segment["text"].strip()
            lines.append(f"[{start}-{end}] {text}")
        else:
            lines.append(segment["text"].strip())

    return lines


def process_video(video_path, output_folder, include_timestamps=False):
    """
    Process a video file to generate audio and subtitles.
    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Path where output files will be saved.
        include_timestamps (bool): Whether to include timestamps in subtitles.
    """
    os.makedirs(output_folder, exist_ok=True)
    print(f"Processing video: {video_path}")

    # Prepare paths
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    audio_file = os.path.join(output_folder, f"{video_name}.wav")
    subtitle_file = os.path.join(output_folder, f"{video_name}.txt")

    # Remove existing subtitle file
    if os.path.exists(subtitle_file):
        os.remove(subtitle_file)

    # Extract audio
    print("Extracting audio...")
    audio_file = extract_audio(video_path, output_folder)
    print(f"Audio saved: {audio_file}")

    # Transcribe audio
    print(f"Transcribing audio: {audio_file}")
    lines = transcribe_audio(audio_file, include_timestamps)

    # Save subtitles
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Subtitles saved: {subtitle_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process video files to audio and subtitles."
    )
    parser.add_argument(
        "uri", type=str, help="Input resource URI: local file path or video URL (YouTube, etc.)."
    )
    parser.add_argument(
        "--timestamps", action="store_true", help="Include timestamps in subtitles."
    )
    args = parser.parse_args()

    uri = args.uri
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(project_root, "files")

    # Ensure the files directory exists
    os.makedirs(output_folder, exist_ok=True)

    if is_youtube_url(uri):
        from youtube_downloader import download
        try:
            video_path = download(uri, output_folder)
            if video_path:
                process_video(video_path, output_folder, include_timestamps=args.timestamps)
        except Exception as e:
            print(f"Error: {e}")
    elif os.path.isfile(uri):
        process_video(uri, output_folder, include_timestamps=args.timestamps)
    else:
        print(f"Input not found or not supported: {uri}")
