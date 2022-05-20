import numpy as np
import cv2
import pyrealsense2.pyrealsense2 as rs
from camera_constants import DCCACameraConstants

class RGBDRealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()

        self.camera_constants = DCCACameraConstants()
        resolution = self.get_resolution()
        framerate = self.get_framerate()
        config.enable_stream(rs.stream.color, resolution[0], resolution[1], rs.format.bgr8, framerate) # if there is an frame drop 30 -> 15 + format is y8
        config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, framerate)

        self.pipeline.start(config)
        align_to=rs.stream.infrared
        self.align = rs.align(align_to)

    def get_resolution(self):
        width = self.camera_constants.FrameWidth
        height = self.camera_constants.FrameHeight
        return [width, height]

    def get_framerate(self):
        framerate = self.camera_constants.FrameRate
        return framerate

    def get_rgbBool(self):
        rgbBool = self.camera_constants.RGB
        return rgbBool
        


    def get_frame_stream(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        rgb_frame = aligned_frames.get_color_frame() # not sure about this

        if not depth_frame or not rgb_frame:
            print("NoFrameError")
            return False, None, None

        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)
        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        # colorizer = rs.colorizer()
        # depth_color_map = np.asanyarray(colorizer.colorize(filled_depth.get_data()))

        depth_image = np.asanyarray(filled_depth.get_data())
        infrared_image = np.asanyarray(rgb_frame.get_data())

        return True, infrared_image, depth_image

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
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha = 0.03), cv2.COLORMAP_JET) 
                    # ir_colomap = cv2.applyColorMap(cv2.convertScaleAbs(ir_img, alpha = 0.03), cv2.COLORMAP_JET) 
                    

                    depth_dim = depth_colormap.shape
                    rgb_dim = rgb_img.shape

                    # print(f"depth_size {depth_dim}, ir_size : {rgb_dim}")
                    if depth_dim != rgb_dim:
                        rgb_img = cv2.resize(rgb_img, dsize = (depth_img[0], depth_img[1], 3))

                        # images = np.stack((rgb_image, depth_img))
                    # else:
                        # images = np.stack((rgb_img, depth_img))

                    cv2.namedWindow("RGBD Camera Experiment - DepthColor", cv2.WINDOW_AUTOSIZE)
                    # cv2.imshow("RGBD Camera Experiment - VanillaDepth", depth_img)
                    cv2.imshow("RGBD Camera Experiment - DepthColor", depth_colormap)

                    
                    cv2.namedWindow("RGBD Camera Experiment- RGB", cv2.WINDOW_AUTOSIZE)
                    cv2.imshow("RGBD Camera Experiment- RGB", rgb_img)
                    cv2.waitKey(1)
                else:
                    print("No Frames")
                    continue
        # except Exception as e:
        #     print(e)

        finally:
            self.release()
            cv2.destroyAllWindows()



if __name__ == "__main__":
    ird = RGBDRealsenseCamera()
    ird.view_by_cv2()



