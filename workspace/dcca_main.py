# 1. Camera Instance를 형성하고 data를 받아옴, (아니면 Camera Data를 얻어오는 subscriber를 생성함)
# 2. Segmentation result를 형성함.
    # 이때 Segmentation은 DepthMap이 아니라, pixel별 classMap
# 3. Object Detection result를 형성함.
    # box내 pixel수 등을 기준으로 정확도 향상
# 4. Class별 Distance Map을 형성함.
    # DistanceDataStructure를 만들자:
        # Class, Distance, LevelOfDangerous, 
# 5. Output을 다듬어서 반환함. (아니면 Info등의 토픽으로 publish함)

from realsense_camera.dcca_camera import RealsenseCamera
from dcca_dataStructure import DCCA_DataStructure

rs = RealsenseCamera()

while True:
    flag, bgr_frame, depth_frame = rs.get_frame_stream()

    boxes, classes, contours, centers = detect(bgr_frame)

    bgr_frame = detect.draw_object_mask(bgr_frame)

    detect.draw_object_info(bgr_frame, depth_frame)

