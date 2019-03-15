import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import compare_mse
from skimage.measure import compare_psnr
from skimage.measure import compare_ssim

def compare_mse(origin, target):
    diff=origin.astype("float") - target.astype("float")
    return np.square(diff).sum() / (origin.shape[0]*origin.shape[1])


if __name__ == "__main__":
    origin_img = cv2.imread("test1.jpg")
    target_img = cv2.imread("test2.jpg")
    mse=compare_mse(origin_img, target_img)
    print("MSE: {}".format(mse))
    psnr=compare_psnr(origin_img, target_img)
    print("PSNR: {}".format(psnr))
    ssim=compare_ssim(cv2.cvtColor(origin_img, cv2.COLOR_BGR2GRAY),
        cv2.cvtColor(target_img, cv2.COLOR_BGR2GRAY))
    print("SSIM: {}".format(ssim))
