#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:09:01 2021

@author: SumeetKumar
"""

import numpy as np

def read_tecfile(filepath):
    '''
    accepts filepath to *.tec file and returns an array of all the data within it 
    
    Parameters
    ----------
    filepath : str
        complete filepath of the *.tec file

    Returns
    ----------
    Data_arr : ndarray
    '''
    with open(filepath) as f:
        Data_all=[]
        for line in f:
            row_data=[]
            for t in line.split():
                try:
                    row_data.append(float(t))     #extract data in line only if it is floating point
                except ValueError:
                    pass
            if row_data:    #if non-empty
                Data_all.append(row_data)
    Data_arr = np.array(Data_all)
    return Data_arr

def read_tecfile_OASPLdB(filepath):
    '''
    accepts filepath to *.tec file and returns an array OASPL data within it in dB 
    
    Parameters
    ----------
    filepath : str
        complete filepath of the *.tec file

    Returns
    ----------
    Data_arr : ndarray
                 
    '''
    with open(filepath) as f:
        Data_all=[]
        for line in f:
            row_data=[]
            for t in line.split():
                try:
                    row_data.append(float(t))     #extract data in line only if it is floating point
                except ValueError:
                    pass
            if row_data:    #if non-empty
                Data_all.append(row_data)
    Data_arr = np.array(Data_all)
    return Data_arr.tolist()
