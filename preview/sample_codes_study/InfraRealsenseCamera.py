import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2

class InfraRealsenseCamera:
    def __init__(self):
        self.pipeline = rs.pipeline()
        config = rs.config()
        # config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_stream(rs.stream.infrared, 640, 480, rs.format.y8, 6) # if there is an frame drop 30 -> 15 + format is y8
        

        self.pipeline.start(config)
        
        # MAYBE : we do not need aligining since we are using only one channel
        #self.align = rs.align(align_to_certain_streaming)
            
    def __str__(self):
        return "This is Vanilla mode for realsense d430 camera"

    def get_frame_stream(self):
        # Stream DepthFrame
        frames = self.pipeline.wait_for_frames()
        ir_frame = frames.get_infrared_frame()

        if not ir_frame:
            print("NoFrameError!")
            return False, None

        # fill the potential holes in depth frame
        # visualize depth objects by colors
        ir_image = np.asanyarray(ir_frame.get_data())
        print(f"cur type is : {type(ir_image)} and internal type is : {ir_image.dtype}")
        return True, ir_image

    def release(self):
        self.pipeline.stop()

if __name__ == "__main__":
    ir = InfraRealsenseCamera()
    try:
        while True:

            flag, ir_img = ir.get_frame_stream()
            ir_colormap = cv2.applyColorMap(cv2.convertScaleAbs(ir_img, alpha = 0.03), cv2.COLORMAP_JET) 


            if flag:

                cv2.namedWindow("IRD Camera Experiment", cv2.WINDOW_AUTOSIZE)
                cv2.imshow("IRD Camera Experiment", ir_img)
                # cv2.imshow("IRD Camera Experiment", ir_colormap)

                cv2.waitKey(1)
            else:
                print("No Frames")
                continue
    except Exception as e:
        print(e)

    finally:
        ir.release()
        cv2.destroyAllWindows()


        