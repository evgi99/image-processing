import datetime
import cv2

from constants import NO_MORE_FRAMES_SIGNAL, MIN_AREA_SIZE, KILL_ALL_SIGNAL

"""
This Class (Process) receive frame with frames metadata and contours. The process will:
1. Drew the contours
2. Add Blurring 
3. Add text on the frame
3. Show the video motion detection  
"""


class Presenter:

    # Ctor of the Presenter Object with outputQueue(as input) and main_queue
    def __init__(self, output_queue, main_queue):
        self._output_queue = output_queue
        self._main_queue = main_queue

    def run_job(self):
        last_frame_display_ts = datetime.datetime.now()
        while True:
            frame, time_offset, cnts, signal = self._consume_output_data()
            if signal == NO_MORE_FRAMES_SIGNAL:
                break
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < MIN_AREA_SIZE:
                    continue
                # compute the bounding box for the contour, draw it on the frame
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                frame = self._blur_the_contour(frame, x, y, w, h)

            # Update the frame with text (date)
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 0)

            time_offset = datetime.timedelta(milliseconds=time_offset)
            while datetime.datetime.now() - last_frame_display_ts < time_offset:
                pass

            # show the frames
            cv2.imshow("video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        self._notify_kill()

    def _blur_the_contour(self, frame, x, y, w, h):
        # Blurring the contour's bounding box
        blured = cv2.GaussianBlur(frame[y:y + h, x:x + w], (43, 43), 0)
        frame[y:y + h, x:x + w] = blured
        return frame

    def _consume_output_data(self):
        return self._output_queue.get()

    def _notify_kill(self):
        self._main_queue.put((KILL_ALL_SIGNAL))
