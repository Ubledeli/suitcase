from datetime import datetime
import numpy as np


def date_from_txt(path):
    str2date = lambda x: datetime.strptime(x[:-3], '%Y-%m-%d %H:%M:%S.%f')
    timestamps = np.genfromtxt(path, delimiter=';', converters={0: str2date}, encoding='utf-8')
    return timestamps

