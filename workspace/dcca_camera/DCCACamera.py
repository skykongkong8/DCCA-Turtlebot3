import sys
sys.path.append("..")
from .RGBDRealsenseCamera import RGBDRealsenseCamera
from yolov5.DCCAYoloManager import DCCAYoloManager
from dcca_dataStructure.DCCADataStructure import DCCA_DataStructure
from .dcca_utils import *
import numpy as np
import cv2




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
        self.n_clusters = 3
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


    def data_formulator(self, label, distance):
        data = DCCA_DataStructure(label = label, distance = distance)

        return data



if __name__ == "__main__":
    dcca_camera = DCCACamera()
    try:
        while True:
            flag, rgb_img, depth_img  = dcca_camera.get_frame_stream()
            detected_results = dcca_camera.dcca_yolov5(flag, rgb_img, depth_img, cvView = True)

            # data_lists = []
            # for detected_object in detected_results:
            #     x1, y1, x2, y2 = detected_object[0][0], detected_object[0][1], detected_object[0][2], detected_object[0][3]
            #     label = detected_object[1]
                
            #     # print(f"label : {label}")
            #     # print(f"x1: {x1}\ty1: {y1}\tx2: {x2}\ty2: {y2}\n")

            #     if depth_img.any():
            #         print(f"depth image :\n{depth_img}")
            #         cut_depthImage = cut_Frame(int(x1), int(y1), int(x2), int(y2), depth_img)
            #         print(f"x1: {x1}\ty1: {y1}\tx2: {x2}\ty2: {y2}\n")
            #         if cut_depthImage.any():
            #             print(f"cut image :\n{cut_depthImage}")
            #             final_depth = kmeans_clustering(cut_depthImage)
            #             DCCA_data = dcca_camera.data_formulator(label, final_depth)
            #             print(f"DCCA Data:\n{DCCA_data}")
            #             data_lists.append(DCCA_data)
            #     print(f"DCCA DataStructure has created! : {data_lists}")
    finally:
        dcca_camera.release()


