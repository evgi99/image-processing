import cv2

from constants import NO_MORE_FRAMES_SIGNAL


def video_reader(vidio_path, frames_queue):
    """
    This function read the original video and send to video processing
    frame-by-frame.
    """
    video_capture = cv2.VideoCapture(vidio_path)
    if video_capture is None or not video_capture.isOpened():
        print("Warning: unable to open video source: '{}', check with os.path.exists()".format(vidio_path))

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        if not ret:
            frames_queue.put((None, NO_MORE_FRAMES_SIGNAL))
            break
        frames_queue.put((frame, ""))
