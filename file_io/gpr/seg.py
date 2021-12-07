import os

import segyio
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
import struct
from astropy.coordinates import Angle, Longitude, Latitude
from astropy import units as u


def load_segy(file_path):
    with segyio.open(file_path, strict=False, endian='little') as f:
        longitudes = []
        global_longitudes = []
        raw = f.trace.raw[:].T
        for i in range(f.header.length):
            scalar = f.header[i].buf[70:72]
            long = f.header[i].buf[72:76]
            lat = f.header[i].buf[76:80]
            global_long = f.header[i].buf[182:190]
            units = f.header[i].buf[88:90]
            scalar = struct.unpack('>h', scalar)[0]
            units = struct.unpack('>h', units)[0]
            lo = struct.unpack('>f', long)[0]
            la = struct.unpack('>f', lat)[0]
            glo_lo = struct.unpack('>d', global_long)[0]
            # longitudes.append(long)
            # global_longitudes.append(global_long)
            longitudes.append(lo)
            global_longitudes.append(glo_lo)
        longitudes = np.array(longitudes)
        global_longitudes = np.array(global_longitudes)
        # print(f'min: {longitudes.min()}, max: {longitudes.max()}, global_min: {global_longitudes.min()}, global_max: {global_longitudes.max()}')
        if units > 1:
            # print(f'arc seconds: {lo}, global: {global_long}')
            try:
                # longitude_angle = Angle(f'{str(lo)[:2]}h{str(lo)[2:]}m')
                # latitude_angle = Angle(f'{str(la)[:2]}h{str(la)[2:]}m')
                la_a = Angle(f'{str(la)}m').deg
                lo_a = Angle(f'{str(lo)}m').deg
                print(f'{lo_a}, {la_a}')
            except:
                print(la, lo)
        # else:
            # print(f'meters or feets: {lo}, global: {global_long}')
        # print(units, scalar)
        return raw


def all_segys(sgy_folder, img_folder):
    files = sorted(os.listdir(sgy_folder))
    for file in files:
        # segy_path = Path(f'{folder}/{file}')
        stem = Path(f'{file}').stem
        data = load_segy(f'{sgy_folder}/{file}')

        # mean = data.mean(axis=1)[..., None]
        # std = data.std(axis=1)[..., None]
        # data = (data - mean) / (std + 1e-6)

        vmin = np.percentile(data, 5)
        vmax = np.percentile(data, 95)

        # vmin = data[128:, :].min()
        # vmax = data[128:, :].max()
        plt.imsave(f'{img_folder}/{stem}.png', data, vmin=vmin, vmax=vmax)
        # plt.imsave(f'{img_folder}/{stem}.png', data)
        # plt.imshow(data)
        # plt.show()


if __name__ == '__main__':
    sgy_folder = f'/home/matija/code/segy/sgy'
    img_folder = f'/home/matija/code/segy/images'
    all_segys(sgy_folder, img_folder)
    # four_byte = '/home/matija/code/segy/sgy/se-70 sn7078.SGY'
    # data = load_segy(four_byte)
    # plt.imshow(data)
    # plt.show()
    print('done')
