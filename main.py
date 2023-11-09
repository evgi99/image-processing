import multiprocessing as mp
import argparse

from constants import PATH_TO_DEFAULT_VIDEO
from streamer import Streamer
from detector import Detector
from presenter import Presenter

if __name__ == '__main__':
    # initialize video_url from user args, if empty the default is 'People - 6387.mp4'
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", default=PATH_TO_DEFAULT_VIDEO, help="path to the video file")
    args = vars(ap.parse_args())
    video_url = args["video"]

    # initialize queue for communication between processes
    frames_queue = mp.Queue()
    out_queue = mp.Queue()
    main_queue = mp.Queue()

    # initialize process objects
    streamer_obj = Streamer(video_url, frames_queue)
    detector_obj = Detector(frames_queue, out_queue)
    presenter_obj = Presenter(out_queue, main_queue)

    # initialize the processes
    reader_worker = mp.Process(target=streamer_obj.run_job)
    processing_worker = mp.Process(target=detector_obj.run_job)
    video_printer_worker = mp.Process(target=presenter_obj.run_job)

    # start to program
    reader_worker.start()
    processing_worker.start()
    video_printer_worker.start()

    # when done, terminate all processes
    is_done = main_queue.get()
    reader_worker.terminate()
    processing_worker.terminate()
    video_printer_worker.terminate()
