"""

THIS FILE IS TO SHOW DCCA YOLO MANAGER ON REMOTE REPOSITORY !
THIS FILE WOULD NEVER WORK IN ACTUAL PRACTICE

"""













#!/usr/bin/env python
import os, sys
import cv2
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import time
from pathlib import Path
import torch
import torch.backends.cudnn as cudnn
import math

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())

from models.experimental import attempt_load
from utils.dataloaders import LoadStreams, LoadImages
from utils.augmentations import Albumentations, augment_hsv, copy_paste, letterbox, mixup, random_perspective
from utils.general import check_img_size, check_requirements, check_imshow, colorstr, non_max_suppression, \
    apply_classifier, scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path #,save_one_box
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync#, load_classifier

class DCCAYoloManager:
    """
    Manager for big or little settings for yolov5 detection in DCCA,
    Stores every function w.r.t. yolov5,
    get resolution as input!
    """
    """
    Bearing in mind that:

    Everything would work simultaneously in a single timeline at DCCA_relay.py,
    DCCAYoloManager works at DCCACamera, getting webcam streaming from RGBDCamera as input!
    
    """
    def __init__(self, resolution):
        self.resolution = resolution # e.g. (640, 640)
        
        self.weights = 'yolov5s.pt' # path where model resides
        self.imgsz = resolution[0] # inference pixel size + NEEDS VERIFICATION
        self.conf_thres = 0.25 # confidence threshold
        self.iou_thres = 0.45 # NMS IOU threshold
        self.max_det = 10 # maximum detections per image
        self.classes = None # filter by class: --class 0, or --class 0 2 3
        self.agnostic_nms = False # class-agnostic NMS
        self.augment = False # augmented inference
        self.visualize = False # visualize  features
        self.line_thickness = 3 # bounding box line thickness (pixelwise thickness)
        self.hide_labels = False # hide labels
        self.hide_conf = False # hide confidences
        self.half = False # use FP16 half-precision inference
        self.stride = 32
        self.device_num = '' # cuda device e.g. 0, or cpu

        self.view_img = False # show results
        self.save_crop = False # save cropped prediction boxes
        self.nosave = False # do not save images
        self.update = False # update all models
        name = 'exp' # save results to project/name     

    @torch.no_grad()
    def get_model(self):

        # Initialization
        set_logging()
        device = select_device(self.device_num)
        self.half &= device.type != 'cpu' # half precision only supported on CUDA

        # Load Model
        model = attempt_load(self.weights, map_location = device) # load FP32 model
        self.stride = int(model.stride.max()) # set model stride
        self.imgsz = check_img_size(self.imgsz, s = self.stride) # check image size
        names = model.module.names if hasattr(model, 'module') else model.names # get class names
        if self.half:
            model.half()
        
        # If using second-stage classifier, set classify = True (optional)
        classify = False
        # if classify:
            # modelc = load_classifier(name='resnet50', n = 2) # second model init
            # modelc.load_state_dict(torch.load('resnet50.pt', map_location = device)['model']).to(device).eval()

        # Dataloader
        view_img = check_imshow()
        cudnn.benchmark = True

        # Run inference
        if device.type != 'cpu':
            model(torch.zeros(1, 3, self.imgsz, self.imgsz).to(device).type_as(next(model.parameters())))

        """
                # SKIP image getting part since we are getting it from DCCACamera
        """
        return [model, device, names]

    @torch.no_grad()
    def process_model_in_loop(self, rgb_image, model, device, names): # model, device, names come from
        t0 = time.time()

        s = np.stack([letterbox(x, self.imgsz, stride = self.stride)[0].shape for x in rgb_image], 0)
        rect = np.unique(s, axis = 0).shape[0] == 1
        if not rect:
            print("WARNING : Different stream shapes are detected. For optimal performance, we recommend you to supply similarly-shaped images")
        
        # Letterbox shaping
        rgb_image0 = rgb_image.copy()
        rgb_image = rgb_image[np.newaxis, :, :, :]
        
        # Stacking
        rgb_image = np.stack(rgb_image, 0)

        # Converting
        rgb_image = rgb_image[..., ::-1].transpose((0,3,1,2)) # BGR to RGB, BHWC to BCHW
        rgb_image = np.ascontiguousarray(rgb_image)

        rgb_image = torch.from_numpy(rgb_image).to(device)
        rgb_image = rgb_image.half() if self.half else rgb_image.float()
        rgb_image /= 255.0 # normalization
        if rgb_image.ndimension() == 3:
            rgb_image = rgb_image.unsqueeze(0)
        
        # Inference
        t1 = time_sync()
        pred = model(rgb_image, augment= self.augment, 
        visualize = increment_path(save_dir / 'features', mkdir=True) if self.visualize else False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, self.classes, self.agnostic_nms, max_det = self.max_det)
        t2 = time_sync()

        
        # Apply Second clf (optional) --needs extra code revision : get params from self.get_model()
        # if classify:
            # pred = apply_classifier(pred, modelc, rgb_image, rgb_image0)
        
        # Process detected results

        detected_results = []
        for i, det in enumerate(pred):
            s = f"{i}: "
            s += "%gx%g " % rgb_image.shape[2:]
            annotator = Annotator(rgb_image0, line_width = self.line_thickness, example = str(names))
            if len(det):
                # Rescale boxes from img_size to image0 size
                det[:, :4] = scale_coords(rgb_image.shape[2:], det[:, :4], rgb_image0.shape).round()

                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()
                    s += f"{n} {names[int(c)]}{'s'*(n>1)}, "

                for *xyxy, conf, cls in reversed(det):
                    c = int(cls)
                    label = None if self.hide_labels else (names[c] if self.hide_conf else f"{names[c]} {conf:.2f}")
                    annotator.box_label(xyxy, label, color=colors(c, True))

                    if not self.hide_labels:
                        detected_results.append([xyxy, label])

        return rgb_image0, detected_results

    def view_detection_and_depth(self, rgb_image0, depth_image):
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.imshow("DCCACamera DepthColor", depth_colormap)

        cv2.imshow("DCCACamera yolov5 detection", rgb_image0)

        cv2.waitKey(1)

