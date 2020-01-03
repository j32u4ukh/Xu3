# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 07:51:09 2019

@author: j32u4ukh
"""
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.math import (
    add,
    subtract,
    multiply,
    divide,
    pow as tf_pow,
    reduce_mean as tf_mean,
    reduce_std as tf_std
)
from skimage import metrics

from Xu3.utils import (
    showImages,
    multiOperation
)


def ssim(x, y, is_normalized=False):
    """
    l(x, y) = (2 * ux * uy + c1) / (ux^2 + uy^2 + c1)
    c(x, y) = (2 * std_x * std_y + c2) / (std_x^2 + std_y^2 + c2)
    s(x, y) = (std_xy + c3) / (std_x * std_y + c3)

    c1 = (k1 * L)^2
    c2 = (k2 * L)^2
    L:像素範圍，2^B - 1(1 or 255)
    c3 = c2 / 2
    k1 = 0.01
    k2 = 0.03

    ssim = l(x, y)^alpha * c(x, y)^beta * s(x, y)^gama

    cov(x, y) = E(x * y) - ux * uy

    而在實際應用中，一般采用高斯函數計算圖像的均值、方差以及協方差，
    而不是采用遍歷像素點的方式，以換來更高的效率。
    """
    k1 = 0.01
    k2 = 0.03
    L = 1.0 if is_normalized else 255.0
    c1 = np.power(k1 * L, 2)
    c2 = np.power(k2 * L, 2)
    c3 = c2 / 2

    ux = x.mean()
    uy = y.mean()

    std_x = x.std()
    std_y = y.std()

    xy = (x - ux) * (y - uy)
    std_xy = xy.mean()

    l_xy = (2 * ux * uy + c1) / (np.power(ux, 2) + np.power(uy, 2) + c1)
    c_xy = (2 * std_x * std_y + c2) / (np.power(std_x, 2) + np.power(std_y, 2) + c2)
    s_xy = (std_xy + c3) / (std_x * std_y + c3)

    return l_xy * c_xy * s_xy


def tfSsim(x, y, is_normalized=False):
    """
    k1 = 0.01
    k2 = 0.03
    L = 1.0 if is_normalized else 255.0
    c1 = np.power(k1 * L, 2)
    c2 = np.power(k2 * L, 2)
    c3 = c2 / 2
    """
    k1 = 0.01
    k2 = 0.03
    L = 1.0 if is_normalized else 255.0
    c1 = tf_pow(multiply(k1, L), 2.0)
    c2 = tf_pow(multiply(k2, L), 2.0)
    c3 = divide(c2, 2.0)

    #     if type(x) is np.ndarray:
    #          x = tf.convert_to_tensor(x, dtype=tf.float32)
    #     if type(y) is np.ndarray:
    #          y = tf.convert_to_tensor(y, dtype=tf.float32)

    """
    ux = x.mean()
    uy = y.mean()
    """
    ux = tf_mean(x)
    uy = tf_mean(y)

    """
    std_x = x.std()
    std_y = y.std()
    """
    std_x = tf_std(x)
    std_y = tf_std(y)

    """
    xy = (x - ux) * (y - uy)
    std_xy = xy.mean()
    """
    xy = multiply(subtract(x, ux), subtract(y, uy))
    std_xy = tf_mean(xy)

    """
    l_xy = (2 * ux * uy + c1) / (np.power(ux, 2) + np.power(uy, 2) + c1)
    """
    l_son = add(multiOperation(multiply, 2.0, ux, uy), c1)
    l_mom = multiOperation(add, tf_pow(ux, 2.0), tf_pow(uy, 2.0), c1)
    l_xy = divide(l_son, l_mom)

    """
    c_xy = (2 * std_x * std_y + c2) / (np.power(std_x, 2) + np.power(std_y, 2) + c2)
    """
    c_son = add(multiOperation(multiply, 2.0, std_x, std_y), c2)
    c_mom = multiOperation(add, tf_pow(std_x, 2.0), tf_pow(std_y, 2.0), c2)
    c_xy = divide(c_son, c_mom)

    """
    s_xy = (std_xy + c3) / (std_x * std_y + c3)
    """
    s_son = add(std_xy, c3)
    s_mom = add(multiply(std_x, std_y), c3)
    s_xy = divide(s_son, s_mom)

    return multiOperation(multiply, l_xy, c_xy, s_xy)


if __name__ == "__main__":
    img = cv2.imread("data/image/lenna.png")
    img2 = img.copy()
    dst = cv2.GaussianBlur(img, (11, 11), 0)
    showImages(origin=img, blur=dst)

    print("ssim(img, img2):", ssim(img, img2))
    print("ssim(img, dst):", ssim(img, dst))
    print("structural_similarity(img, img2):", metrics.structural_similarity(
        img,
        img2,
        multichannel=True,
        data_range=255))
    print("structural_similarity(img, dst):", metrics.structural_similarity(
        img,
        dst,
        multichannel=True,
        data_range=255))

    # img.dtype = np.float32
    # img2.dtype = np.float32
    # dst.dtype = np.float32

    x = tf.placeholder(dtype=tf.float32,
                       shape=[None, None, 3])
    y = tf.placeholder(dtype=tf.float32,
                       shape=[None, None, 3])
    init = tf.global_variables_initializer()
    compute_ssim = tfSsim(x, y)
    compute_add = add(x, y)

    with tf.Session() as sess:
        sess.run(init)
        ssim_value = sess.run(compute_ssim,
                              feed_dict={x: img,
                                         y: img2})

        ssim_value = sess.run(compute_ssim,
                              feed_dict={x: img,
                                         y: dst})
        print("ssim_value:", ssim_value)
