import cv2
import imutils

from constants import NO_MORE_FRAMES_SIGNAL

"""
This Class (Process) receive frame with frames metadata in order to process the frame:
1. Detect counter
2. Add Blurring 
3. Send the frame metadata with the process's enrichment
"""


class Detector:

    # Ctor of the Detector Object with framesQueue(input) and outputQueue
    def __init__(self, frames_queue, output_queue):
        self._frames_queue = frames_queue
        self._output_queue = output_queue

    def run_job(self):
        prev_frame = None

        while True:
            # receive frame information from the queue
            frame, time_offset, signal = self._consume_frame_data()

            # in case of no more frames to process
            if signal == NO_MORE_FRAMES_SIGNAL:
                self._push_frame_data(None, None, [], signal)
                break

            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # if it is the first frame (mean prev is None), initialize it
            if prev_frame is None:
                prev_frame = gray_frame
                self._push_frame_data(frame, time_offset, [], None)
            else:
                # This algorithm on how we find contours have been given with the requirements.
                # more info:
                # https://pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/

                diff = cv2.absdiff(gray_frame, prev_frame)
                thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                prev_frame = gray_frame
                self._push_frame_data(frame, time_offset, cnts, None)

    def _push_frame_data(self, frame, time_offset, contours, signal):
        self._output_queue.put((frame, time_offset, contours, signal))

    def _consume_frame_data(self):
        return self._frames_queue.get()
