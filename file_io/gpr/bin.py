import numpy as np
import matplotlib.pyplot as plt
import time
# import struct

start_code = b'\x80\x00\x00\x00\x00\x00'


def parse(byte_stream):
    traces = []
    skip = 0
    while skip < len(byte_stream):
        start = byte_stream[skip:].find(start_code)
        trace = byte_stream[skip + start + 12: skip + start + 12 + 512 * 3]  # just data
        # trace = byte_stream[skip + start + 0: skip + start + 18 + 512 * 3]  # everything, including start and stop
        skip += 6 + 512 * 3
        traces.append(trace)
    return traces


if __name__ == '__main__':
    with open('data', 'rb') as f:
        out = f.read()

    traces = parse(out)

    data = []
    for trace in traces[:-1]:  # discard incomplete trace
        numbers = []
        for i in range(0, len(trace), 3):
            decoded = int.from_bytes(trace[i: i+3], 'big')

            # decoded = trace[i +0] << 16 | trace[i +1] << 8 | trace[i +2]
            # decoded = struct.unpack('>i', b'\x00'+trace[i: i+3])[0]
            numbers.append(decoded)
        data.append(numbers)

    data = np.array(data).T

    vmin = np.percentile(data, 5)
    vmax = np.percentile(data, 95)

    plt.imsave(f'B-scan.png', data, vmin=vmin, vmax=vmax)
    print('done')
