#!/usr/bin/env python
# encoding: utf-8

# The MIT License

# Copyright (c) 2021 Ina (David Doukhan & Zohra Rezgui- http://www.ina.fr/)

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

import dlib
import cv2
import pylab as plt
from .face_utils import extract_right_eye_center, extract_left_eye_center, _angle_between_2_points#, get_rotation_matrix
import numpy as np
from tensorflow.keras.utils import get_file


class Dlib68FaceAlignment:
    """
    Methods for detecting eye centers based on Dlib's set of 68 facial landmarks
    this information may be used to rotate the input image such as the eyes lie
    on a horizontal line
    Aligned faces allow to obtain better results on face classication tasks
    """

    def __init__(self, verbose=False):
        """
        Load dlib's 68 facial landmark detection model

        Parameters
        ----------
        verbose : boolean, optional. The default is False.
            If set to True, resulting rotated image will be displayed.
        """
        url_r2 = 'https://github.com/ina-foss/inaFaceGender/releases/download/models-init-2/'
        fname = get_file('shape_predictor_68_face_landmarks.dat', url_r2 + 'shape_predictor_68_face_landmarks.dat')
        self.model = dlib.shape_predictor(fname)
        self.verbose = verbose

    def detect_eye_centers(self, frame, bb):
        """
        Detects left and right eye centers

        Parameters
        ----------
        frame : numpy.ndarray (height,with, 3)
            RGB image data
        bb : (x1, y1, x2, y2) or None
            Location of the face in the frame
            If set to None, the whole image is considered as a face

        Returns
        -------
        left_eye : (x,y)
            Center of the left eye in the input image
        right_eye : (x,y)
            Center of the right eye in the input image

        """
        if bb is None:
            bb = (0, 0, frame.shape[1], frame.shape[0])
        bb = dlib.rectangle(*bb)
        shape = self.model(frame, bb)
        left_eye = extract_left_eye_center(shape)
        right_eye = extract_right_eye_center(shape)
        return left_eye, right_eye

    def __call__(self, frame, bb):
        """
        Performs eye centers detection and rotate image such as the eyes lie
        on a horizontal line

        Parameters
        ----------
        frame : numpy.ndarray (height,with, 3)
            RGB image data
        bb : (x1, y1, x2, y2) or None
            Location of the face in the frame
            If set to None, the whole image is considered as a face

        Returns
        -------
        rotated_frame : numpy.ndarray (height,with, 3)
            RGB rotated image data
        left_eye : (x,y)
            Center of the left eye in the input image
        right_eye : (x,y)
            Center of the right eye in the input image

        """
        left_eye, right_eye = self.detect_eye_centers(frame, bb)
        w = bb[2] - bb[0]
        h = bb[3] - bb[1]

        angle = _angle_between_2_points(left_eye, right_eye)
        xc = (left_eye[0] + right_eye[0]) / 2
        yc = (left_eye[1] + right_eye[1]) / 2
        M = cv2.getRotationMatrix2D((xc, yc), angle, 1)
        M += np.array([[0, 0, -bb[0]], [0, 0, -bb[1]]])


        rotated_frame = cv2.warpAffine(frame, M, (w, h), flags=cv2.INTER_CUBIC)

        if self.verbose:
            print('after rotation')
            plt.imshow(rotated_frame)
            plt.show()
        return rotated_frame, left_eye, right_eye
