import time
from threading import Thread

import cv2

from dodge_game.camera.transforms import distort_image
from dodge_game.camera.webcamstream import WebcamStream
from camera_controller import CameraController


class CameraControllerHandler:

    # initialization method
    def __init__(self, webcam_stream_id, camera_width, camera_height, level_timer):
        self.level_timer = level_timer
        # initializing and starting multi-threaded webcam input stream
        self.webcam_stream = WebcamStream(
            stream_id=webcam_stream_id,
            camera_width=camera_width,
            camera_height=camera_height,
        )  # 0 id for main camera
        self.webcam_stream.start()  # processing frames in input stream

        self.stopped = True  # thread instantiation
        self.t = Thread(target=self.run_webcam_controller, args=())
        self.t.daemon = True  # daemon threads run in background

        # Outputs of the camera controller
        self.image = self.webcam_stream.read()  # Get the initial image

        self.x = camera_width
        self.y = camera_height

        self.fps = 0
        self.cam_fps = self.webcam_stream.fps_input_stream

    # method to start thread
    def start(self):
        self.stopped = False
        self.t.start()  # method passed to thread to read next available frame

    def run_webcam_controller(self):
        # Create the webcam controller in the same thread as the camera controller
        webcam_controller = CameraController()

        while True:
            if self.stopped is True:
                break

            start = time.time()

            webcam_image = self.webcam_stream.read()

            # Flip the frame such that left is left on the screen
            webcam_image = cv2.flip(webcam_image, 1)

            # Transform the image
            transforms = self.level_timer.get_level_settings()["image_transforms"]
            image = distort_image(webcam_image, transforms=transforms)

            # Get the location from the webcam controller
            self.x, self.y, self.image = webcam_controller.get_location(image)

            end = time.time()
            elapsed = end - start
            vid_pros_fps = 1 / elapsed

            # The real fps is limited by the camera fps
            self.fps = min(self.cam_fps, vid_pros_fps)

            # Kinda hacky:
            self.level_timer.v_fps = self.fps

    def get_image(self):
        return self.image

    def get_fps(self):
        return self.fps

    def stop(self):
        self.stopped = True
