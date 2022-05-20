from dataclasses import dataclass
import pyrealsense2.pyrealsense2 as rs

"""
[ CAMERA CONSTANTS ]

* This file includes all basic settings / hard-code needed information of Intel RealSense Camera connected to the DCCA Agent.
Please add constants you need below whenever you code it. *

<CAMERA CONSTANTS>
- frame width
- frame hieght
- fps
- device product line
- whether rgb channel is possible or not

"""



"""
**RESOLUTION TUNING TRIAL LOG!** 

[WARNING] : this is only subjective assessment, so it might vary under your environment or purpose...
[example DEVICE] : IntelRealsense D435 + NVDIA Jetson Nano

HD : not working

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
# FRAME_WIDTH = 600
# FRAME_HEIGHT = 800

# # VGA resolution - (affordable)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# # QVGA resolution
# FRAME_WIDTH = 320
# FRAME_HEIGHT = 240

# 240p resolution
# FRAME_WIDTH = 426
# FRAME_HEIGHT = 240

"""
**FRAME RATE TUNING TRIAL LOG!**

[WARNING] : this is only subjective assessment, so it might vary under your environment or purpose...
[example DEVICE] : IntelRealsense D435 + NVDIA Jetson Nano

120 : not working

100 : not working

90 : not working

60 : doable

30 : not bad

15 : least working
"""
FRAME_RATE = 60 # aka, FPS

def device_checker():
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

    """
    [ DCCA CAMERA CONSTANTS ]

    - FrameWidth
    - FrameHeight
    - FrameRate
    - RGB
    - DeviceProductLine

    """

    # DCCACameraConstants class attribute naming rule:
    # - No Underbar 
    # - Capital letter for every new word
    # - Specify the datatype
    
    FrameWidth : int = FRAME_WIDTH
    FrameHeight : int = FRAME_HEIGHT
    FrameRate : int = FRAME_RATE

    device_info = device_checker() # this is not an intended attribute
    RGB : bool = device_info[0]
    DeviceProductLine : str = device_info[1]
    

if __name__ == "__main__":
    cameraconstant = DCCACameraConstants()
    print(cameraconstant)


