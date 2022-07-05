from dcca_camera.DCCACamera import DCCACamera
from dcca_camera.RGBDRealsenseCamera import RGBDRealsenseCamera
from dcca_camera.dcca_utils import cut_Frame, kmeans_clustering



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
                
                if depth_img.any():
                    print(f"depth image :\n{depth_img}")
                    cut_depthImage = cut_Frame(int(x1), int(y1), int(x2), int(y2), depth_img)
                    print(f"x1: {x1}\ty1: {y1}\tx2: {x2}\ty2: {y2}\n")

                    if cut_depthImage.any():
                        print(f"cut image :\n{cut_depthImage}")
                        final_depth = kmeans_clustering(cut_depthImage)
                        DCCA_data = dcca_camera.data_formulator(label, final_depth)
                        print(f"DCCA Data:\n{DCCA_data}")
                        data_lists.append(DCCA_data)

                print(f"DCCA DataStructure has created! : {data_lists}")

    except Exception as e:
        print(e)
    finally:
        dcca_camera.release()