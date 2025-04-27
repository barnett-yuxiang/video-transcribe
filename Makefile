# Unit tests
test:
	PYTHONPATH=. pytest -v

# Manual YouTube download test (requires Chrome logged in to YouTube)
# Usage: make yt-download url='https://www.youtube.com/watch?v=IHNzOHi8sJs'
yt-download:
	yt-dlp --cookies-from-browser chrome -f 18 "$(url)"

# List all available formats for the given YouTube video
# Usage: make yt-list-formats url='https://www.youtube.com/watch?v=IHNzOHi8sJs'
yt-list-formats:
	yt-dlp -F "$(url)"

# Show video stream info (resolution, codec, framerate) for a local file
# Usage: make ffprobe-video file=./files/IHNzOHi8sJs.mp4
ffprobe-video:
	ffprobe -v error -show_streams -select_streams v:0 -show_entries stream=width,height,codec_name,avg_frame_rate "$(file)"

# Show audio stream info (codec, channels, sample rate, bitrate) for a local file
# Usage: make ffprobe-audio file=./files/IHNzOHi8sJs.mp4
ffprobe-audio:
	ffprobe -v error -show_streams -select_streams a:0 -show_entries stream=codec_name,channels,sample_rate,bit_rate "$(file)"

# Format Python code using isort and black
format:
	isort .
	black .

# Check code style without making changes
check-format:
	isort --check-only .
	black --check .
