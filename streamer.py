import cv2
import datetime

from constants import NO_MORE_FRAMES_SIGNAL

"""
This Class (Process) read the original video and send to video processing
frame-by-frame and keep the fps rate.
"""


class Streamer:

    # Ctor of the Streamer Object with path to file and the Queue
    def __init__(self, path_to_file, frames_queue):
        self._video_path = path_to_file
        self._frames_queue = frames_queue

    def run_job(self):
        # handle the video capturing from the video file
        video_capture = cv2.VideoCapture(self._video_path)
        if video_capture is None or not video_capture.isOpened():
            print(f"Warning: unable to open video source: '{self._video_path}', check with os.path.exists()")

        # handle the frames per second value
        fps_of_video = video_capture.get(cv2.CAP_PROP_FPS)

        # initialize the array of timestamps with the first step at 0.0
        calc_timestamps = [0.0]

        while True:
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            if not ret:
                # send only the signal in order to notify about NO-MORE frames to process
                self._push_frame_data(None, None, NO_MORE_FRAMES_SIGNAL)
                break

            # calculate the offset and frame starting time to keep the correct rate
            time_offset = calc_timestamps[-1] + 1000 / fps_of_video
            calc_timestamps.append(time_offset)

            # Push all the frame metadata to the queue
            self._push_frame_data(frame, time_offset, None)

        video_capture.release()

    def _push_frame_data(self, frame, time_offset, signal):
        self._frames_queue.put((frame, time_offset, signal))
