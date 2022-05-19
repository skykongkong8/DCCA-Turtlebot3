import numpy as np
import cv2
import pyrealsense2.pyrealsense2 as rs
from camera_constants import DCCACameraConstants

class IRDRealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()

        resolution = self.get_resolution()
        config.enable_stream(rs.stream.infrared, resolution[0], resolution[1], rs.format.y8, 15) # if there is an frame drop 30 -> 15 + format is y8
        config.enable_stream(rs.stream.depth, resolution[0], resolution[1], rs.format.z16, 15)

        self.pipeline.start(config)
        align_to=rs.stream.infrared
        self.align = rs.align(align_to)

    def get_resolution(self):
        camera_constants = DCCACameraConstants()
        width = camera_constants.FrameWidth
        height = camera_constants.FrameHeight
        return [width, height]

    def get_frame_stream(self):
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        infrared_frame = aligned_frames.get_infrared_frame() # not sure about this

        if not depth_frame or not infrared_frame:
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
        infrared_image = np.asanyarray(infrared_frame.get_data())

        return True, infrared_image, depth_image

    def release(self):
        self.pipeline.stop()
        print("Terminate Everything...")

    def view_by_cv2(self):
        print("THIS IS FOR VISUAL CHECKING!")
        try:
            while True:

                flag, ir_img, depth_img = self.get_frame_stream()

                if flag:
                    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_img, alpha = 0.03), cv2.COLORMAP_JET) 
                    # ir_colomap = cv2.applyColorMap(cv2.convertScaleAbs(ir_img, alpha = 0.03), cv2.COLORMAP_JET) 
                    

                    depth_dim = depth_img.shape
                    ir_dim = ir_img.shape

                    # print(f"depth_size {depth_dim}, ir_size : {ir_dim}")
                    if depth_dim != ir_dim:
                        resized_ir_image = cv2.resize(ir_img, dsize = (depth_img[0], depth_img[1]))

                        images = np.stack((resized_ir_image, depth_img))

                    else:
                        images = np.stack((ir_img, depth_img))

                    cv2.namedWindow("IRD Camera Experiment - DepthColor", cv2.WINDOW_AUTOSIZE)
                    # cv2.imshow("IRD Camera Experiment - DepthColor", depth_img)
                    cv2.imshow("IRD Camera Experiment - DepthColor", depth_colormap)

                    
                    cv2.namedWindow("IRD Camera Experiment- IR", cv2.WINDOW_AUTOSIZE)
                    cv2.imshow("IRD Camera Experiment- IR", ir_img)
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
    ird = IRDRealsenseCamera()
    ird.view_by_cv2()



