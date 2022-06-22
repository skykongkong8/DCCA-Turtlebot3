import sys
sys.path.append("..")
from RGBDRealsenseCamera import RGBDRealsenseCamera
from yolov5.DCCAYoloManager import DCCAYoloManager



class DCCACamera(RGBDRealsenseCamera):
    """
    DCCACamera contains: 
    RGB/Depth Streaming, 
    Object Detection, 
    Object Depth Clustering,
    Final Distancing and DCCA DataStructure Formulation
    """
    def __init__(self):
        super().__init__()
        print("RGBCamera Initialized...")
        self.yoloManager = DCCAYoloManager(self.get_resolution())
        model_setting = self.yoloManager.get_model()
        self.model = model_setting[0]
        self.device = model_setting[1]
        self.names = model_setting[2]
        print("DCCACamera Initialized...")

    def yolov5(self, cvView = False):
        flag, rgb_img, depth_img = self.get_frame_stream()
        if flag:
            detected_image = self.yoloManager.process_model_in_loop(rgb_img, self.model, self.device, self.names)

            if cvView:
                self.yoloManager.view_by_cv2(detected_image, depth_img)


if __name__ == "__main__":
    dcca_camera = DCCACamera()
    try:
        while True:
            dcca_camera.yolov5(cvView = True)
    # except Exception as e:
    #     print(e)
    finally:
        dcca_camera.release()


