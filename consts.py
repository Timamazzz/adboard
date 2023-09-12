import cv2
import numpy as np

GENDER_MODEL = 'models/gender_deploy.prototxt'
GENDER_PROTO = 'models/gender_net.caffemodel'

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
GENDER_LIST = ['Male', 'Female']

FACE_PROTO = "models/gender_deploy.prototxt.txt"
FACE_MODEL = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
