import time

import cv2
import matplotlib.pyplot as plt
import numpy as np
import onnxruntime as ort
import torch
import torch.nn as nn
import torch.nn.functional as F


class Fused(nn.Module):
    def __init__(self, seg_model):
        super(Fused, self).__init__()
        self.patch = Patch()
        self.segformer = seg_model

    def forward(self, img):
        img = F.interpolate(img[0], size=(4*512, 7*512), mode='bilinear', align_corners=True)
        patches = self.patch(img)
        patches = patches[0].permute(3, 0, 1, 2)
        out = self.segformer([patches])
        out = self.custom_fold(out.float())[None, None, ...]
        out = F.interpolate(out, size=(2160, 3840), mode='bilinear', align_corners=True)
        return out

    @staticmethod
    def custom_fold(img):
        empty = torch.zeros(size=(4 * 512, 7 * 512))
        for i in range(4):
            for j in range(7):
                empty[i * 512: (i + 1) * 512, j * 512: (j + 1) * 512] = img[0, i * 7 + j]
        return empty


class Patch(nn.Module):
    def __init__(self, kernel=512, stride=512):
        super(Patch, self).__init__()
        self.kernel = kernel
        self.stride = stride

    def forward(self, img):
        patches = F.unfold(img, kernel_size=self.kernel, stride=self.stride)
        patches = patches.reshape(img.shape[0], img.shape[1], self.kernel, self.kernel, -1)
        return patches


def export_patches(kernel=512, stride=512, width=3840, height=2160):
    model = Patch(kernel=kernel, stride=stride)
    dummy_input = torch.randn(1, 3, height, width, device='cuda')
    input_names = ['input']
    output_names = ["output"]
    dynamic_axes = {'input': {0: 'batch'}, 'output': {0: 'batch', 4: 'patches'}}
    torch.onnx.export(model, dummy_input, "patches.onnx", verbose=False, input_names=input_names,
                      output_names=output_names, dynamic_axes=dynamic_axes, opset_version=11)


def split_image():
    model = Patch(kernel=512, stride=512)
    img = cv2.imread('8185-ortho.jpg')
    img = cv2.resize(img, (512, 512))
    img = torch.tensor(img).permute(2, 0, 1)[None, ...].float()  # / 255
    patches = model(img)
    for i in range(patches.shape[-1]):
        p = patches[0, ..., i].permute(1, 2, 0)
        cv2.imwrite(f'{i}.jpg', p.numpy())
        # cv2.imshow(' ', p.numpy())
        # cv2.waitKey(0)

