import os
import whisper

def transcribe_videos(input_folder, output_folder, model_name="base"):
    """
    Transcribe video files in the input_folder and save the results as .txt files in the output_folder.

    Args:
        input_folder (str): Path to the folder containing video files.
        output_folder (str): Path to the folder to save transcribed .txt files.
        model_name (str): Whisper model name to use for transcription. Default is 'base'.
    """
    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model(model_name)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each video file in the input folder
    for file_name in os.listdir(input_folder):
        input_file_path = os.path.join(input_folder, file_name)

        # Skip non-video files
        if not file_name.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
            print(f"Skipping non-video file: {file_name}")
            continue

        print(f"Processing file: {file_name}")

        # Perform transcription
        result = model.transcribe(input_file_path)

        # Save the transcription to a .txt file
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.txt")
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(result['text'])

        print(f"Transcription saved: {output_file_path}")

if __name__ == "__main__":
    # Define paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(project_root, "files")
    output_folder = project_root

    # Run the transcription process
    transcribe_videos(input_folder, output_folder)
