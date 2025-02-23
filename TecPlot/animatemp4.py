#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 12:53:46 2022

@author: ge56beh
"""
import tecplot as tp
import glob
import subprocess
import glob
import os
from PIL import Image



def png_to_movie(directry, basename, animation_dict):
    """
    https://hamelot.io/visualization/using-ffmpeg-to-convert-a-set-of-images-into-a-video/

    """
    
    framerate = animation_dict['animspeed']
    images = glob.glob("{}/{}*.png".format(directry,basename))
    im = Image.open(images[0])
    width, height = im.size
    filepattern = f'{directry}/'+"{}_{}.png".format(basename, '%06d')
    
    # dimensions must be even values
    dimension = "{}x{}".format(int(width/2)*2, int(height/2)*2)
    args = ["ffmpeg",
            "-framerate", str(framerate),
            # "-filter \"minterpolate=\'fps=30\'\" ",
            "-y",   # overwrite if mp4 file with same name already exists
            "-i", filepattern,
            "-s:v", dimension,
            "-c:v", "libx264",
            "-profile:v", "high",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            f'{directry}/{basename}.mp4']
    
    # quick error handling for ffmpeg in the PATH
    try:
        subprocess.run(args)
    except FileNotFoundError as e:
        print(e)
        print("make_movie: This error is likely due to ffmpeg not being in your PATH.")
        print("make_movie: Please add the Tecplot bin directory to your PATH to use ffmpeg.")

    for pngfile in images: os.remove(pngfile)










    
    
