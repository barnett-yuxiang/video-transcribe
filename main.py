import os
import ffmpeg
import whisper
from datetime import timedelta
import argparse


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
    Extract entire audio from a video file as a single WAV file.

    Args:
        video_path (str): Path to the video file.
        output_path (str): Path to save the audio file.

    Returns:
        str: Path to the generated audio file.
    """
    audio_file = os.path.join(
        output_path, f"{os.path.splitext(os.path.basename(video_path))[0]}.wav"
    )
    ffmpeg.input(video_path).output(
        audio_file, format="wav", acodec="pcm_s16le", ac=1, ar="16000"
    ).run(quiet=True)
    return audio_file


def transcribe_audio(model, audio_path, include_timestamps=False):
    """
    Transcribe audio file to subtitles with accurate timestamps.

    Args:
        model: Whisper model.
        audio_path (str): Path to the audio file.
        include_timestamps (bool): Whether to include timestamps in the output.

    Returns:
        list: Transcribed text lines with optional timestamps.
    """
    result = model.transcribe(audio_path, word_timestamps=True)
    segments = result.get("segments", [])

    lines = []
    for segment in segments:
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"].strip()

        if include_timestamps:
            lines.append(
                f"[{format_timestamp(start_time)}-{format_timestamp(end_time)}] {text}"
            )
        else:
            lines.append(text)

    return lines


def process_video(
    video_path, output_folder, model_name="base", include_timestamps=False
):
    """
    Process a video file to generate audio and subtitles.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Path to save the output files.
        model_name (str): Whisper model name.
        include_timestamps (bool): Whether to include timestamps in subtitles.
    """
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

    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model(model_name)

    # Transcribe audio
    print(f"Transcribing audio: {audio_file}")
    lines = transcribe_audio(model, audio_file, include_timestamps)

    # Save subtitles
    with open(subtitle_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Subtitles saved: {subtitle_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process video files to audio and subtitles."
    )
    parser.add_argument(
        "--timestamps", action="store_true", help="Include timestamps in subtitles."
    )
    args = parser.parse_args()

    # Define paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(project_root, "files")
    output_folder = input_folder

    # Process each video in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
            video_path = os.path.join(input_folder, file_name)
            process_video(video_path, output_folder, include_timestamps=args.timestamps)
