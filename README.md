# Camera Recorder Application with Human Detection

This Python application allows you to record video from your computer's camera and save it as an MP4 file. It utilizes OpenCV library and YOLO (You Only Look Once) object detection algorithm for human detection.

## Requirements

- Python 3.x
- OpenCV library (`pip install opencv-python`)
- Pre-trained YOLO model: yolov3.cfg and yolov3.weights (`https://pjreddie.com/darknet/yolo/`)
- VLC media player (or any other compatible media player) to play the recorded videos
- ffmpeg (command-line tool) for video extraction (`https://ffmpeg.org/download.html`)

## Installation

1. Clone the repository or download the source code files.

2. Download the pre-trained YOLO model:
   - Create a folder named "yolo" in the same directory as the Python script.
   - Download the YOLO configuration file (`yolov3.cfg`), pre-trained weights file (`yolov3.weights`)
   - Place these files in the "yolo" folder.

3. Install the required Python packages:
   ```
   pip install opencv-python numpy
   ```

4. Ensure you have VLC media player (or another compatible media player) installed on your system to play the recorded videos.

5. Install ffmpeg (command-line tool) from the official website: `https://ffmpeg.org/download.html`. Make sure ffmpeg is accessible from the command line.

## Usage

1. Create a directory named "records" in the same directory as the Python script.

2. Run the Python script `camera_recorder.py` to record video using the camera recorder application. The recorded videos will be saved in the "records" folder.

3. Run the Python script `human_detection.py` to process the recorded videos.

4. The script will scan the "records" folder for video files.

5. For each video file, the script will perform human detection using YOLO and extract the portions where humans are present.

6. The detected portions of the videos will be saved as separate MP4 files in the "output" folder. Each output file will have a name format of "video_timestamp_human.mp4" (e.g., "video_2023-07-06_11-52-34_human.mp4").

7. The script will print the time intervals when humans are detected in each video file, along with the paths of the generated output files.

8. To play the recorded videos, open them using VLC media player (or another compatible media player).