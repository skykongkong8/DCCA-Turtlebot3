import sys
sys.path.append("..")
from RGBDRealsenseCamera import RGBDRealsenseCamera
from yolov5.DCCAYoloManager import DCCAYoloManager
from yolov5.recognition_with_realsense import run



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

    def dcca_yolov5(self, cvView = False):
        flag, rgb_img, depth_img = self.get_frame_stream()
        if flag:
            detected_img = self.yoloManager.process_model_in_loop(rgb_img, self.model, self.device, self.names)

            if cvView:
                self.yoloManager.view_detection_and_depth(detected_img, depth_img)

    def _psuedo_recognition_with_realsense(self):
        run()


if __name__ == "__main__":
    dcca_camera = DCCACamera()
    try:
        while True:
            dcca_camera.dcca_yolov5(cvView = True)
        # dcca_camera._recognition_with_realsense()
    # except Exception as e:
    #     print(e)
    finally:
        dcca_camera.release()


