## Ground penetrating radar  
[Official docs](https://www.dropbox.com/sh/5kgy9gf7kj3ds8l/AACvDvarBf0RnDclS4C4XIn5a?dl=0)


## Get raw data over bluetooth

#### Install necessary (bluetooth) tools:
```
sudo apt install bluez bluez-tools

sudo apt install blueman

pip install pyserial
```

#### Set up bluetooth connection:
```
sudo service bluetooth restart  # (optional) 
blueman-manager
```
right-click on a device -> Connect to -> Serial port

#### Get data over bluetooth:
```
python3 gpr.py 
```
file 'data' will appear on Desktop.

## Convert binary data to B-scan
produces an image: 'B-scan.png'
```
python3 bin.py
```

## Convert .sgy files to images
(change input and output paths)
```
python3 seg.py
```