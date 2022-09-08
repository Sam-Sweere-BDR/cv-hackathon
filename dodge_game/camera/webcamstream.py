# defining a helper class for implementing multi-threading
# Based on: https://gvasu.medium.com/faster-real-time-video-processing-using-multi-threading-in-python-8902589e1055

import time
from threading import Thread

import cv2


class WebcamStream:

    # initialization method
    def __init__(self, stream_id, camera_width, camera_height):
        self.stream_id = stream_id  # default is 0 for main camera

        # Set the camera resolution and fps for a level and speedy playingfield
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.cam_fps = 30

        # opening camera capture stream
        self.vcap = cv2.VideoCapture(self.stream_id)
        self.vcap.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.vcap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_width)
        self.vcap.set(cv2.CAP_PROP_FPS, self.cam_fps)

        if self.vcap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        self.fps_input_stream = int(self.vcap.get(5))  # hardware fps
        print("FPS of input stream: {}".format(self.fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.vcap.read()
        if self.grabbed is False:
            print("[Exiting] No more frames to read")
            exit(0)  # self.stopped is initialized to False
        self.stopped = True  # thread instantiation
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads run in background

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()  # method passed to thread to read next available frame

    def update(self):
        while True:
            if self.stopped is True:
                break
            self.grabbed, self.frame = self.vcap.read()

            if self.grabbed is False:
                print("[Exiting] No more frames to read")
                self.stopped = True
                break
        self.vcap.release()  # method to return latest read frame

    def read(self):
        return self.frame  # method to stop reading frames

    def stop(self):
        self.stopped = True


if __name__ == "__main__":
    # In my case:
    # device_num = 0 for internal webcam
    # device_num = 4 for external webcam

    # initializing and starting multi-threaded webcam input stream
    webcam_stream = WebcamStream(stream_id=4)  # 0 id for main camera
    webcam_stream.start()  # processing frames in input stream
    num_frames_processed = 0
    start = time.time()
    while True:
        if webcam_stream.stopped is True:
            break
        else:
            frame = (
                webcam_stream.read()
            )  # adding a delay for simulating camera processing time
        delay = 0.01  # delay value in seconds
        time.sleep(delay)
        num_frames_processed += 1  # displaying frame
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
    end = time.time()
    webcam_stream.stop()  # stop the webcam stream

    # printing time elapsed and fps
    elapsed = end - start
    fps = num_frames_processed / elapsed
    print("FPS: {} , Elapsed Time: {} ".format(fps, elapsed))  # closing all windows
    cv2.destroyAllWindows()
