import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2

# almost always start with :\
pipeline = rs.pipeline()
config = rs.config()

# get device product line info for resolution settings
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))


# find if there is any rgb camera
found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == "RGB CAMERA":
        found_rgb = True
        break

if not found_rgb:
    print("Current demo needs a Depth Camera with RGB sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream_color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream_color, 640, 480, rs.format.bgr8, 30)


# streaming start!
pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue
        
        # convert images to np arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())


        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha = 0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize = (depth_colormap_dim[1], depth_colormap_dim[0]), interpolation = cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow("RealSenseHMS", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense HMS", images)
        cv2.waitKey(1)

except Exception as e:
    print(e)
finally:
    pipeline.stop()

