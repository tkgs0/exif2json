#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from sys import version_info as vf
if not (vf.major == 3 and vf.minor >= 8):
    print('\033[40;33;1mOnly for Python >= 3.8\033[0m')
    exit(-1)


from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from PIL import Image
from PIL.ExifTags import TAGS
import time


filepath = (Path(__file__).parent / '..').rglob(r'*.*')
outpath = Path(__file__).parent / 'exif.json'


start = time.time()
print('loading...')
x = 0
n = len(filepath := list(filepath))

content = dict()
for pic in filepath:
    x += 1
    y = int(float(x) / n * 20)
    print(
        f"\r[{'='*y}{' '*(20-y)}] {y*5}% {time.time()-start:.2f}s",
        end=' ', flush=True
    )
    try:
        img = Image.open(pic).getexif()
    except Exception as e:
        continue
    tags = dict()
    for k,v in img.items():
        tag = TAGS.get(k,k)
        if isinstance(v, tuple):
            v = list(v)
        elif isinstance(v, bytes):
            v = v.decode('unicode-escape').replace('\x00', '')
        elif not isinstance(v, int):
            v = str(v)
        tags.update({tag: v})
    content.update({pic.name: tags})


outpath.write_text(
    json.dumps(content, indent=2, ensure_ascii=False),
    encoding='utf-8'
)

print('done.')
