from dataclasses import dataclass
import pyrealsense2.pyrealsense2 as rs

"""
**RESOLUTION TUNING TRIAL LOG!** 

[WARNING] : this is only subjective assessment, so it might vary under your environment or purpose...
[example DEVICE] : IntelRealsense D430 Module + NVDIA Jetson Nano

HD : extreme latency...

SVGA : not working

WVGA : not working

VGA : minimum latency, affordable!

QVGA : not working

240p : not working
"""
# HD (720p) resolution - (highest feasible)
# FRAME_WIDTH = 1280
# FRAME_HEIGHT = 720

# # SVGA resolution
# FRAME_WIDTH = 800
# FRAME_HEIGHT = 600

# # WVGA resolution
# FRAME_WIDTH = 800
# FRAME_HEIGHT = 600

# # VGA resolution - (affordable)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# # QVGA resolution
# FRAME_WIDTH = 320
# FRAME_HEIGHT = 240

# 240p resolution
# FRAME_WIDTH = 426
# FRAME_HEIGHT = 240


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
class DCCACameraConstants:
    FrameWidth : int = FRAME_WIDTH
    FrameHeight : int = FRAME_HEIGHT
    RGB : bool = rgb_checker()[0]
    device_product_line : str = rgb_checker()[1]

if __name__ == "__main__":
    cameraconstant = DCCACameraConstants()
    print(cameraconstant)


