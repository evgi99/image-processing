import cv2
import imutils

from constants import NO_MORE_FRAMES_SIGNAL


def video_detector_process(frames_queue, out_queue):
    counter = 0
    prev_frame = None

    while True:
        frame, signal = frames_queue.get()
        if signal == NO_MORE_FRAMES_SIGNAL:
            out_queue.put((frame, [], signal))
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if counter == 0:
            prev_frame = gray_frame
            counter += 1
            out_queue.put((frame, [], ""))
        else:
            diff = cv2.absdiff(gray_frame, prev_frame)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            prev_frame = gray_frame
            counter += 1
            out_queue.put((frame, cnts, ""))
