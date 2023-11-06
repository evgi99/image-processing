import multiprocessing as mp
import argparse

from streamer import video_reader
from detector import video_detector_process
from presentor import video_printer

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
