import os
import whisper
import ffmpeg
from math import ceil
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


def transcribe_video_segment(
    model, video_path, start_time, duration, interval, include_timestamps
):
    """
    Transcribe a specific segment of a video file.

    Args:
        model: Whisper model for transcription.
        video_path (str): Path to the video file.
        start_time (float): Start time of the segment in seconds.
        duration (float): Duration of the segment in seconds.
        interval (int): Interval in seconds for splitting text segments.
        include_timestamps (bool): Whether to include timestamps in the output.

    Returns:
        list of str: Transcribed text lines with optional timestamps.
    """
    temp_audio_path = "temp_audio.wav"

    # Extract audio for the segment
    ffmpeg.input(video_path, ss=start_time, t=duration).output(
        temp_audio_path, format="wav"
    ).run(quiet=True)

    # Transcribe the audio
    result = model.transcribe(temp_audio_path, word_timestamps=True)
    os.remove(temp_audio_path)  # Clean up temporary file

    # Organize transcription into 2-second segments
    lines = []
    current_time = start_time
    segment_text = []

    for word_info in result["segments"]:
        word_start = word_info["start"]
        word_text = word_info["text"]

        if word_start >= current_time + interval:
            if include_timestamps:
                lines.append(
                    f"[{format_timestamp(current_time)}] {' '.join(segment_text)}"
                )
            else:
                lines.append(" ".join(segment_text))
            segment_text = []
            current_time += interval

        segment_text.append(word_text)

    # Add the last segment
    if segment_text:
        if include_timestamps:
            lines.append(f"[{format_timestamp(current_time)}] {' '.join(segment_text)}")
        else:
            lines.append(" ".join(segment_text))

    return lines


def transcribe_videos(
    input_folder,
    output_folder,
    model_name="base",
    segment_size_mb=5,
    interval=2,
    include_timestamps=False,
):
    """
    Transcribe video files in the input_folder and save subtitles as .txt files.

    Args:
        input_folder (str): Path to the folder containing video files.
        output_folder (str): Path to save transcribed .txt files.
        model_name (str): Whisper model name to use for transcription.
        segment_size_mb (int): Maximum size of each segment in MB.
        interval (int): Interval in seconds for splitting text segments.
        include_timestamps (bool): Whether to include timestamps in the output.
    """
    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model(model_name)

    # Process each video file in the input folder
    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)

        # Skip non-video files
        if not file_name.lower().endswith((".mp4", ".mkv", ".avi", ".mov")):
            print(f"Skipping non-video file: {file_name}")
            continue

        print(f"Processing file: {file_name}")

        # Prepare the output .txt file path
        output_file_path = os.path.join(
            output_folder, f"{os.path.splitext(file_name)[0]}.txt"
        )
        if os.path.exists(output_file_path):
            os.remove(output_file_path)  # Clean previous results

        # Get video duration and size
        video_info = ffmpeg.probe(input_file_path)
        duration = float(video_info["format"]["duration"])  # In seconds
        file_size = float(video_info["format"]["size"]) / (1024 * 1024)  # In MB
        segment_duration = duration / (file_size / segment_size_mb)

        # Process the video in segments
        start_time = 0
        while start_time < duration:
            current_duration = min(segment_duration, duration - start_time)
            if current_duration < interval and start_time + current_duration < duration:
                # Merge with the next segment if the remainder is too short
                current_duration += interval

            print(
                f"Transcribing segment: Start={start_time:.2f}s, Duration={current_duration:.2f}s"
            )

            # Transcribe the segment
            lines = transcribe_video_segment(
                model,
                input_file_path,
                start_time,
                current_duration,
                interval,
                include_timestamps,
            )

            # Append the transcription to the output file
            with open(output_file_path, "a", encoding="utf-8") as output_file:
                output_file.write("\n".join(lines) + "\n\n")

            start_time += current_duration

        print(f"Transcription saved: {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe video files into text subtitles."
    )
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help="Include timestamps in the output subtitles.",
    )
    args = parser.parse_args()

    # Define paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(project_root, "files")
    output_folder = input_folder

    # Run the transcription process
    transcribe_videos(
        input_folder, output_folder, interval=2, include_timestamps=args.timestamps
    )
