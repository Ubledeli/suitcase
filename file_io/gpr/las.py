import laspy
import csv
import pandas as pd
import open3d as o3d
import numpy as np
csv_names = ['easting', 'northing', 'alt', 'Z', 'GPStime', 'zone_number', 'zone_letter', 'pol']

if __name__ == '__main__':
    # las = laspy.read('norway-k1.las')
    # xyz = np.array([las.x, las.y, las.z]).transpose()

    df = pd.read_csv('parsecual_cli/20210625_183952_012_S_RAW_UTM_ELL_wP.astralite.csv')
    xyz_pol = np.array([df.easting, df.northing, df.alt, df.pol]).transpose()
    # np.histogram(xyz_pol[:, 2], bins=100)[1][62:64]
    # np.histogram(xyz[:, 2], bins=100)[0].argmax()
    hist, bins = np.histogram(xyz_pol[:, 2], bins=122)
    low, high = bins[hist.argmax()], bins[hist.argmax()+1]
    # boundaries = bins[hist.argmax(): hist.argmax()+2]
    top = xyz_pol[xyz_pol[:, 2] >= high]
    bot = xyz_pol[xyz_pol[:, 2] <= low]
    xyz = xyz_pol[xyz_pol[:, 2] < high]

    xyz = xyz[low < xyz[:, 2]]  #

    top_pcd = o3d.geometry.PointCloud()
    top_pcd.points = o3d.utility.Vector3dVector(top[:, :3])
    bot_pcd = o3d.geometry.PointCloud()
    bot_pcd.points = o3d.utility.Vector3dVector(bot[:, :3])
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz[:, :3])
    pcd.paint_uniform_color([1, 0.706, 0])
    top_pcd.paint_uniform_color([0, 0.706, 1])
    bot_pcd.paint_uniform_color([1, 0, 0.706])

    o3d.visualization.draw_geometries([pcd, top_pcd, bot_pcd])
    print('done')