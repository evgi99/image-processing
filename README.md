# image-processing
My first project at Computer Vision.

Basic motion detection and tracking with Python and OpenCV
The system includes 3 processes, each process has one responsibility:

   1. The Streamer - load video from video_url and send the video frame by frame to the Detector.

   2. The Detector - apply the motion detection algorithm on the received frame, then pass the frame with the additional data to the Presenter.

   3. The Presenter - draw the detection on the received frame and show all the frames keeping on the correct fps.

>[!NOTE]  
>Our multiprocessing inter-process communication will be via Queue.

## How to run

### Create and Activate the Virtual Environment
[On macOS and Linux]:

```
python3 -m venv myenv
source myenv/bin/activate
```

### Setup (Install all packages):
```
pip install -r requirements.txt 
```

### Run the program
   
 (with default video)
  ```
  python main.py
  ```
 (with your video)
  ```
  python main.py --video "videos/car-detection.mp4"
  ```


