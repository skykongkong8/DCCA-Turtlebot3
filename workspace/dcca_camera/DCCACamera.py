import sys
sys.path.append("..")
from RGBDRealsenseCamera import RGBDRealsenseCamera
from yolov5.DCCAYoloManager import DCCAYoloManager
import cv2
# from yolov5.recognition_with_realsense import run



class DCCACamera(RGBDRealsenseCamera):
    """
    DCCACamera contains: 
    RGB/Depth Streaming, 
    Object Detection, 
    Object Depth Clustering and Distancing,
    DCCA DataStructure Formulation
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

    def dcca_yolov5(self, flag, rgb_img, depth_img, cvView = False):
        """
        Detects object and returns label and crop box coordinates in xyxy convention
        """
        
        detected_results = []
        # print(f"DEPTH SIZE : {depth_img.shape") -> (240, 320)
        # print(f"RGB SIZE : {rgb_img.shape}") -> (480, 640, 3) 
        depth_img = cv2.resize(depth_img, dsize = (640, 480))
        if flag:
            detected_img, detected_results = self.yoloManager.process_model_in_loop(rgb_img, self.model, self.device, self.names)
            """
            detected_results = [
                ...
                [ [ x1, y1, x2, y2 ], label]
                ...
            ]
            **x1, y1... are tensors
            """
            if cvView:
                self.yoloManager.view_detection_and_depth(detected_img, depth_img)

        return detected_results

    def cut_depthFrame(self, x1, y1, x2, y2, depth_img):
        pass
        
        
            


    # def _psuedo_recognition_with_realsense(self):
    #     run()


if __name__ == "__main__":
    dcca_camera = DCCACamera()
    try:
        while True:
            flag, rgb_img, depth_img  = dcca_camera.get_frame_stream()
            detected_results = dcca_camera.dcca_yolov5(flag, rgb_img, depth_img, cvView = True)
            for detected_object in detected_results:
                x1, y1, x2, y2 = detected_object[0][0], detected_object[0][1], detected_object[0][2], detected_object[0][3]
                label = detected_object[1]
                print(f"label : {label}")
                print(f"x1: {x1}\ty1: {y1}\tx2: {x2}\ty2: {y2}\n")


        # dcca_camera._recognition_with_realsense()
    # except Exception as e:
    #     print(e)
    finally:
        dcca_camera.release()


