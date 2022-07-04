import sys
sys.path.append("..")
from RGBDRealsenseCamera import RGBDRealsenseCamera
from yolov5.DCCAYoloManager import DCCAYoloManager
from dcca_dataStructure.DCCADataStructure import DCCA_DataStructure
from sklearn.cluster import KMeans
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
        cut_depthImage = depth_img[y1:y2, x1:x2]

        cv2.imshow("cut image", cut_depthImage)
        cv2.waitKey(1)

        return cut_depthImage

    def cluster_depths(self, image):
        """
        1. 인식한 물체를 기준으로 좌우상단, 좌우하단, 본체 이렇게 군집화될 것을 예상해서 n = 5
        2. 인식한 물체의 상하만 생각해서 n = 3

        클러스터링 후 가장 큰 클러스터의 평균을 거리로서 활용
        """
        n_clusters = 3
        kmeans = KMeans(n_clusters = n_clusters)
        original_r, original_c = image.shape[0], image.shape[1]
        image = image.reshape(-1,1)
        kmeans.fit(image)

        labels = kmeans.labels_
        target = np.bincount(x).argmax()

        total_distance = 0.
        total_count = 0.
        for i in range(image):
            if labels[i] == target:
                total_count += 1
                total_distance += image[i]

        final_distance = 0.
        if toal_count != 0:
            final_distance = total_distance / total_count
        
        return final_distance

    def data_formulator(self, label, distance):
        data = DCCA_DataStructure(label = label, distance = distance)

        return data   


if __name__ == "__main__":
    dcca_camera = DCCACamera()
    try:
        while True:
            flag, rgb_img, depth_img  = dcca_camera.get_frame_stream()
            detected_results = dcca_camera.dcca_yolov5(flag, rgb_img, depth_img, cvView = True)

            data_lists = []
            for detected_object in detected_results:
                x1, y1, x2, y2 = detected_object[0][0], detected_object[0][1], detected_object[0][2], detected_object[0][3]
                label = detected_object[1]
                
                # print(f"label : {label}")
                # print(f"x1: {x1}\ty1: {y1}\tx2: {x2}\ty2: {y2}\n")
                
                cut_depthImage = dcca_camera.cut_depthFrame(x1, y1, x2, y2, depth_img)
                final_depth = dcca_camera.cluster_depths(cut_depthImage)
                data = dcca_camera.data_formulator(label, final_depth)
                data_lists.append(data)
            print(data_lists)

                


                



        # dcca_camera._recognition_with_realsense()
    # except Exception as e:
    #     print(e)
    finally:
        dcca_camera.release()


