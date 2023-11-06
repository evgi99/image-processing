import datetime
import cv2

from constants import NO_MORE_FRAMES_SIGNAL


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
        cv2.imshow("video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()