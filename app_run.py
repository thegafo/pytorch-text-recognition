import torch
import torch.nn as nn 
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from PIL import Image
import skimage

import cv2
from skimage import io 
import numpy as np 
import json 
import zipfile
from collections import OrderedDict

import text_reco.models.craft.craft_utils as craft_utils
import text_reco.models.craft.imgproc as img_proc

from text_reco.models.craft.craft import CRAFT
from text_reco.models.craft.craft_reader import CraftReader
from text_reco.boxdetect.box_detection import BoxDetect
from text_reco.models.crnn.crnn_run import CRNNReader

def main():
    crnn = CRNNReader()
    crr = CraftReader('data/test.png')
    boxes, img_res = crr.boxes_detect()
    for _, tmp_box in enumerate(boxes):
        x = int(tmp_box[0][0])
        y = int(tmp_box[0][1])
        w = int(np.abs(tmp_box[0][0] - tmp_box[1][0]))
        h = int(np.abs(tmp_box[0][1] - tmp_box[2][1]))
        tmp_img =  img_res[y:y+h, x:x+w]
        print("SHape dataset {}".format(tmp_img.shape))
        # Transform 
        tmp_img.save( 'data/box_{}.jpeg'.format(_))
        del tmp_img
        tmp_img = Image.open('data/box_{}.jpeg'.format(_))
        tmp_img = crnn.transformer(tmp_img)
        tmp_img = tmp_img.view(1, *tmp_img.size())
        tmp_img = Variable(tmp_img)
        print(crnn.get_predictions(tmp_img))

if __name__ == "__main__":
    main()
