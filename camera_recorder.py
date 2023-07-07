import cv2
import os
import datetime


class CameraRecorder:
    def __init__(self):
        # Create the records folder if it doesn't exist
        if not os.path.exists('records'):
            os.makedirs('records')

        # Create a VideoCapture object
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        # Define the video codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_file = f"records/video_{timestamp}.mp4"
        self.out = cv2.VideoWriter(self.output_file, fourcc, 20.0, (640, 480))

    def record_video(self):
        while True:
            # Read each frame from the camera
            ret, frame = self.cap.read()

            # Write the frame to the video file
            self.out.write(frame)

            # Display the resulting frame
            cv2.imshow('Camera', frame)

            # Stop recording when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the resources
        self.cap.release()
        self.out.release()
        cv2.destroyAllWindows()


# Create an instance of CameraRecorder
recorder = CameraRecorder()

# Call the record_video method
recorder.record_video()
