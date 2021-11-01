#!/usr/bin/env python
# encoding: utf-8

# The MIT License

# Copyright (c) 2019 Ina (Thomas Petit & David Doukhan- http://www.ina.fr/)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# This code is a modification of nlhkh's project face-alignment-dlib
# See github.com/nlhkh/face-alignment-dlib/blob/master/utils.py
# It has been adapted by Thomas PETIT (github.com/w2ex) & David Doukhan


import numpy as np
import dlib
from collections.abc import Iterable

# TODO - this file will be splitted into rect & face_align

def tuple2rect(t):
    return dlib.rectangle(*[int(x) for x in np.round(t)])

def tuple2drect(t):
    return dlib.drectangle(*t)

def intersection_over_union(x, y):
    # intersection over union
    if not isinstance(x, dlib.rectangle) and isinstance(x, Iterable):
        x = tuple2rect(x)
    if not isinstance(y, dlib.rectangle) and isinstance(y, Iterable):
        y = tuple2rect(y)
    inter = x.intersect(y).area()
    union = x.area() + y.area() - inter
    return inter / union


def _extract_eye(shape, eye_indices):
    points = map(lambda i: shape.part(i), eye_indices)
    return list(points)


def _extract_eye_center(shape, eye_indices):
    points = _extract_eye(shape, eye_indices)
    xs = map(lambda p: p.x, points)
    ys = map(lambda p: p.y, points)
    return sum(xs) // 6, sum(ys) // 6


def extract_left_eye_center(shape):
    LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
    return _extract_eye_center(shape, LEFT_EYE_INDICES)


def extract_right_eye_center(shape):
    RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]
    return _extract_eye_center(shape, RIGHT_EYE_INDICES)


def _angle_between_2_points(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 != x2:
        tan = (y2 - y1) / (x2 - x1)
        return np.degrees(np.arctan(tan))
    elif y2 > y1:
        return np.degrees(np.pi / 2)

    else:
        return np.degrees(-np.pi / 2)



# def get_rotation_matrix(p1, p2):
#    angle = _angle_between_2_points(p1, p2)
#    x1, y1 = p1
#    x2, y2 = p2
#    xc = (x1 + x2) // 2
#    yc = (y1 + y2) // 2
#    M = cv2.getRotationMatrix2D((xc, yc), angle, 1)
#    return M
