from dataclasses import dataclass
import pyrealsense2.pyrealsense2 as rs

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

def rgb_checker():
    tmp_pipeline = rs.pipeline()
    tmp_config = rs.config()

    pipeline_wrapper = rs.pipeline_wrapper(tmp_pipeline)
    pipeline_profile = tmp_config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == "RGB Camera":
            found_rgb = True
            break
    return found_rgb, device_product_line

@dataclass
class DCCACameraConstant:
    FrameWidth : int = FRAME_WIDTH
    FrameHeight : int = FRAME_HEIGHT
    RGB : bool = rgb_checker()[0]
    device_product_line = rgb_checker()[1]

if __name__ == "__main__":
    cameraconstant = DCCACameraConstant()
    print(cameraconstant)


