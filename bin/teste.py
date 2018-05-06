#!/usr/bin/python
# -*- encoding: utf-8 -*-
import pyexiv2

import time


inicio = time.time()

metadata = pyexiv2.ImageMetadata('/home/witor/Desktop/teste.jpg')
metadata.read()
a = metadata['Exif.Photo.UserComment'].value




fim = time.time()
print(fim - inicio)


