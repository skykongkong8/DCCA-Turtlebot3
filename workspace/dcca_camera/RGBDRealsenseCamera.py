import numpy as np
import cv2
import pyrealsense2.pyrealsense2 as rs
from camera_constants import DCCACameraConstants
from DCCADepthFilterManager import DCCADepthFilterManager

class RGBDRealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()

        self.camera_constants = DCCACameraConstants()
        self.filter_manager = DCCADepthFilterManager()
        resolution = self.get_resolution()
        framerate = self.get_framerate()

        config.enable_stream(rs.stream.color, resolution[0], resolution[1], rs.format.bgr8, framerate)
        config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, framerate)

        self.pipeline.start(config)
        
        align_to=rs.stream.infrared
        self.align = rs.align(align_to)

    def get_resolution(self):
        width = self.camera_constants.FrameWidth
        height = self.camera_constants.FrameHeight
        return (width, height)

    def get_framerate(self):
        framerate = self.camera_constants.FrameRate
        return framerate

    def get_rgbBool(self):
        rgbBool = self.camera_constants.RGB
        return rgbBool
        
    def apply_DepthFilter(self, depth_frame, filterType= None):
        """
        Applying preprocessing filters on depth_frame # not on depth_ColorMap!
        """
        filtered_depth = self.filter_manager.apply_DepthFilter(depth_frame, filterType)

        return filtered_depth

    def get_frame_stream(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        rgb_frame = aligned_frames.get_color_frame()

        if not depth_frame or not rgb_frame:
            print("NoFrameError")
            return False, None, None

        depth_frame = self.apply_DepthFilter(depth_frame) # if you block out this code : your can observe the effect of the filter

        depth_image = np.asanyarray(depth_frame.get_data())
        rgb_image = np.asanyarray(rgb_frame.get_data())

        return True, rgb_image, depth_image

    def release(self):
        self.pipeline.stop()
        print("Terminate Everything...")

    def view_by_cv2(self):
        print("THIS IS FOR VISUAL CHECKING!")
        
        if not self.get_rgbBool():
            print("[WARNING] : NO RGB FRAME IN CURRENT DEPTH CAMERA!")
            exit(0)
        try:
            while True:

                flag, rgb_img, depth_img = self.get_frame_stream()

                if flag:
                    depth_dim = depth_img.shape
                    rgb_dim = rgb_img.shape

                    # print(f"depth_size {depth_dim}, ir_size : {rgb_dim}")
                    if depth_dim[0] != rgb_dim[0] and depth_dim[1] != rgb_dim[1]:
                        depth_img = cv2.resize(depth_img, dsize = (rgb_dim[1], rgb_dim[0]))

                    # if you don't colorize the depth frame, it is quite cumbersome to observe...
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha = 0.03), cv2.COLORMAP_JET) 

                    cv2.namedWindow("RGBD Camera Experiment - DepthColor", cv2.WINDOW_AUTOSIZE)
                    cv2.imshow("RGBD Camera Experiment - DepthColor", depth_colormap)
                    # cv2.imshow("RGBD Camera Experiment - VanillaDepth", depth_img)
                    
                    cv2.namedWindow("RGBD Camera Experiment- RGB", cv2.WINDOW_AUTOSIZE)
                    cv2.imshow("RGBD Camera Experiment- RGB", rgb_img)
                    cv2.waitKey(1)

                else:
                    print("No Frames")
                    continue

        except Exception as e:
            print(e)

        finally:
            self.release()
            cv2.destroyAllWindows()



if __name__ == "__main__":
    ird = RGBDRealsenseCamera()
    ird.view_by_cv2()



