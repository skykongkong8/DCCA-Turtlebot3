import cv2
import numpy as np
# import matplotlib.pyplot as plt
import pyrealsense2.pyrealsense2 as rs


print(f"Environment ready")

# 1. vanilla detection
class VanillaRealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipleine()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)

        self.pipeline.start(config)
        
        # MAYBE : we do not need aligining since we are using only one channel
        #self.align = rs.align(align_to_certain_streaming)
            
    def __str__(self):
        return "This is Vanilla mode for realsense d430 camera"

    def get_frame_stream(self):
        # Stream DepthFrame
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            print("NoFrameError!")
            return False, None

        # fill the potential holes in depth frame
        spatial = rs.spatial_fiter()
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)

        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(filtered_depth)

        # visualize depth objects by colors
        colorizer = rs.colorizer()
        depth_colormap = np.asanyarray(colorizer.colorize(filled_depth).get_data())

        # Formulate into images format : np array
        depth_image = np.asanyarray(filled_depth.get_data())
        
        return True, depth_image

    def release(self):
        self.pipeline.stop()
        
VanillaCamera = VanillaRealsenseCamera()

