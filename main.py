import datetime
import cv2
import multiprocessing as mp
import imutils
import argparse

NO_MORE_FRAMES_SIGNAL = "NO_MORE_FRAMES"

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


def video_printer(out_queue):
    while True:
        frame, cnts, signal = out_queue.get()
        if signal == NO_MORE_FRAMES_SIGNAL:
            break
        for c in cnts:
            # compute the bounding box for the contour, draw it on the frame
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Blurring the contour's bounding box
            blured = cv2.GaussianBlur(frame[y:y + h, x:x + w], (43, 43), 0)
            frame[y:y + h, x:x + w] = blured

        # Update the frame with text (date)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 0)

        # show the frames
        cv2.imshow("videos", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    args = vars(ap.parse_args())
    if args.get("video", None) is None:
        video_url = 'videos/People - 6387.mp4'
    else:
        video_url = args["video"]
    frames_queue = mp.Queue()
    out_queue = mp.Queue()
    reader_worker = mp.Process(target=video_reader, args=(video_url, frames_queue))
    processing_worker = mp.Process(target=video_detector_process, args=(frames_queue, out_queue))
    video_printer_worker = mp.Process(target=video_printer, args=(out_queue,))
    reader_worker.start()
    processing_worker.start()
    video_printer_worker.start()
    processing_worker.join()
    video_printer_worker.join()
