#!/usr/bin/env python
from camera_constants import N_CLUSTERS
from sklearn.cluster import KMeans
import numpy as np
# import cv2

"""
DCCA utils

DCCA relay 중 유용한 수학적 연산 / 알고리즘 함수들을 저장
"""


def ffill_loop(arr, fill=0):
    # Fill nan vlaues of the image with nearby values
    mask = np.isnan(arr[0])
    arr[0][mask] = fill
    for i in range(1, len(arr)):
        mask = np.isnan(arr[i])
        arr[i][mask] = arr[i-1][mask]
    return arr

def cut_Frame(x1, y1, x2, y2, depth_img):
    cut_depthImage = depth_img[x1:x2,y1:y2]

    # cv2.imshow("cut image", cut_depthImage)
    # cv2.waitKey(1)

    return cut_depthImage

def kmeans_clustering(image):
    """
    1. 인식한 물체를 기준으로 좌우상단, 좌우하단, 본체 이렇게 군집화될 것을 예상해서 n = 5
    2. 인식한 물체의 상하만 생각해서 n = 3

    클러스터링 후 가장 큰 클러스터의 평균을 거리로서 활용
    """

    kmeans = KMeans(n_clusters = N_CLUSTERS)
    original_r, original_c = image.shape[0], image.shape[1]
    image = image.reshape(-1,1)
    kmeans.fit(image)

    labels = kmeans.labels_
    target = np.bincount(labels).argmax()

    total_distance = 0.
    total_count = 0
    for i in range(len(image)):
        if labels[i] == target:
            total_count += 1
            total_distance += image[i]

    if total_count != 0:
        final_distance = total_distance / total_count
    
    return final_distance