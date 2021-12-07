import serial

data = []
for i in range(5):
    try:
        s = serial.Serial(f'/dev/rfcomm{i}', 57600)
        print(f'rfcomm{i}')
        break
    except Exception:
        print(f'skip {i}')

for i in range(10000):
    chunk = s.readline()
    # print(chunk)
    data.append(chunk)

with open('data', 'ab') as f:
    for chunk in data:
        f.write(chunk)
