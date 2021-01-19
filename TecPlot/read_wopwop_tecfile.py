#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 15:35:17 2020

@author: ge56beh
"""
import numpy as np
        
def p_spl(filepath):
    '''
    accepts filepath to *.tec file and returns an array of all the data within it 
    
    Parameters
    ----------
    filepath : str
        complete filepath of the *.tec file

    Returns
    ----------
    Data_arr : numpy array
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

def dB(filepath):
    '''
    accepts filepath to *.tec file and returns an array OASPL data within it in dB 
    
    Parameters
    ----------
    filepath : str
        complete filepath of the *.tec file

    Returns
    ----------
    Data_arr : numpy array
                 
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
