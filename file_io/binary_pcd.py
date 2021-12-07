import struct
import numpy as np
# from mayavi.mlab import points3d, show


def kitti_bin_to_pcd(binFilePath):
    size_float = 4
    list_pcd = []
    with open(binFilePath, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_pcd.append([x, y, z])
            byte = f.read(size_float * 4)
    np_pcd = np.asarray(list_pcd)
    return np_pcd


# def draw_pcd(pcd):
#     points3d(pcd[:, 0], pcd[:, 1], pcd[:, 2], scale_factor=0.1)
#     show()
