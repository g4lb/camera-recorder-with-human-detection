import cv2
import os
import datetime
import subprocess
import numpy as np


class HumanDetection:
    def __init__(self, video_file):
        self.video_file = video_file
        self.net = cv2.dnn.readNetFromDarknet('yolo/yolov3.cfg', 'yolo/yolov3.weights')
        self.layers = self.net.getLayerNames()
        self.output_layers = [self.layers[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.conf_threshold = 0.5
        self.nms_threshold = 0.4

    def detect_human(self):
        cap = cv2.VideoCapture(self.video_file)

        human_detected = False
        start_frame = None
        output_files = []

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            height, width, _ = frame.shape

            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            class_ids = []
            confidences = []
            boxes = []

            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if class_id == 0 and confidence > self.conf_threshold:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.conf_threshold, self.nms_threshold)

            if len(indexes) > 0:
                if not human_detected:
                    human_detected = True
                    start_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            else:
                if human_detected:
                    human_detected = False
                    end_frame = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1

                    if start_frame != end_frame:
                        print(f"Human detected from frame {start_frame} to {end_frame}")
                        output_file = self.write_output_video(start_frame, end_frame)
                        if output_file is not None:
                            output_files.append(output_file)
                    else:
                        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                            # Handle case where human disappears at the end of the video
                            end_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT) - 1
                            print(f"Human detected from frame {start_frame} to {end_frame}")
                            output_file = self.write_output_video(start_frame, end_frame)
                            if output_file is not None:
                                output_files.append(output_file)
                        else:
                            print("No human detected in the specified frames. Skipping output video.")

        cap.release()

        return output_files

    def write_output_video(self, start_frame, end_frame):
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        video_name = os.path.splitext(os.path.basename(self.video_file))[0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = os.path.join(output_dir, f"{video_name}_{timestamp}_human.mp4")

        if start_frame <= end_frame:
            cap = cv2.VideoCapture(self.video_file)
            fps = cap.get(cv2.CAP_PROP_FPS)
            cap.release()

            start_time = datetime.timedelta(seconds=int(start_frame / fps))
            duration = datetime.timedelta(seconds=int((end_frame - start_frame + 1) / fps))

            ffmpeg_command = f'ffmpeg -y -ss {start_time} -i "{self.video_file}" -t {duration} -c copy "{output_file}"'
            subprocess.run(ffmpeg_command, shell=True)

            return output_file

        return None


def process_videos():
    # Create the output folder if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    # Get a list of video files in the records folder
    video_files = [
        f for f in os.listdir('records')
        if os.path.isfile(os.path.join('records', f)) and f.lower().endswith('.mp4')
    ]

    # Process each video file
    for video_file in video_files:
        full_path = os.path.join('records', video_file)
        print(f"Processing video: {full_path}")

        # Create an instance of HumanDetection and detect humans in the video
        detector = HumanDetection(full_path)
        output_files = detector.detect_human()

        if len(output_files) > 0:
            print("Output files:")
            for output_file in output_files:
                print(output_file)


# Run the process_videos function
process_videos()
