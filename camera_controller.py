class CameraController:
    def __init__(self):
        self.camera_id = 0  # Usually: 0 for internal camera, 4 for external camera

    def get_location(self, image):
        # Every frame of the game this function is called given the latest input image

        ################# Write your code here! #################

        # Placeholder x and y location:
        x = 200
        y = 200

        # For debugging, you can output or draw a different image. Note that the output image has to have the same
        # dimensions as the input image

        return x, y, image
