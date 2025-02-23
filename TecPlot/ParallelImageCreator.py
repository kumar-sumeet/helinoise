#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 14:07:51 2022

@author: ge56beh
"""

#animation for blade motion (code taken from https://github.com/Tecplot/handyscripts/blob/master/python/ParallelImageCreator.py)

# import multiprocessing
from concurrent.futures import ProcessPoolExecutor as Pool
import os
import atexit
import tecplot as tp
def initialize_process(layout_file):
    atexit.register(tp.session.stop)
    tp.macro.execute_command("$!FileConfig LoadOnDemand { UNLOADSTRATEGY = MinimizeMemoryUse }")
    tp.load_layout(layout_file)
def save_image(args):
    solution_time, width, supersample, image_file = args
    tp.active_frame().plot().solution_time = solution_time
    tp.export.save_png(image_file, width=width, supersample=supersample)
    return image_file
def animatemp4_multiprocess(directry, basename, animation_dict):
    layoutfile = f"{directry}/{basename}.lay"
    numprocs = os.cpu_count()
    imagewidth = animation_dict['imagewidth']
    supersamplefactor = animation_dict['supersamplefactor']
    endtime = animation_dict['endtime']

    tp.new_layout()
    tp.load_layout(layoutfile)
    solution_times = tp.active_frame().dataset.solution_times
    tp.session.stop()
    # multiprocessing.set_start_method('spawn')

    # Set up the pool with initializing function and associated arguments
    pool = Pool(initializer=initialize_process,
                initargs=(layoutfile,),
                # max_workers = numprocs,   #default to number of processors available
                )
    try:
        job_args = []
        for i, solution_time in enumerate(solution_times):
            if solution_time > endtime: 
                break 
            image_file = f'{directry}/{basename}_' + "%06d.png" % (i)
            job_args.append((solution_time, imagewidth, supersamplefactor, image_file))
        image_files = pool.map(save_image, job_args)
    finally:
        pool.close()
        pool.join()
