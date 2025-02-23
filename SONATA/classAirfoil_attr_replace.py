#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 17:09:05 2021

@author: Sumeet Kumar
"""
import numpy as np

from SONATA.cbm.topo.BSplineLst_utils import BSplineLst_from_dct, \
                                             equidistant_D1_on_BSplineLst#, \
                                             #uniformdeflection_on_BSplineLst
from OCC.Core.Geom import Geom_BSplineCurve
from OCC.Core.Geom2dAdaptor import Geom2dAdaptor_Curve
from OCC.Core.GCPnts import GCPnts_UniformDeflection
from OCC.Core.gp import gp_Pnt2d,gp_Vec2d

def uniformdeflection_on_BSplineLst(BSplineLst, deflection):
    """
    distributes Points and NormalVectors on Geom2d_BSplineLst such that the
    concentration is higher in regions of high curvature
    
    """
    PntLst = []
    VecLst = []
    for item in BSplineLst:
        
        if isinstance(item,Geom_BSplineCurve):
            print('ERROR: Argument must be a Geom2d_BSplineLst')
                       
        Adaptor = Geom2dAdaptor_Curve(item)
        discretization = GCPnts_UniformDeflection(Adaptor,deflection)
        NbPoints = discretization.NbPoints()
        for j in range(1, NbPoints+1):
                para = discretization.Parameter(j)
                Pnt2d = gp_Pnt2d()
                Vec2d = gp_Vec2d()
                item.D1(para, Pnt2d, Vec2d)
                PntLst.append(Pnt2d)
                VecLst.append(Vec2d.GetNormal())
                
    return (PntLst, VecLst)

def gen_wopwop_dist(self,dist_curvature,surfaces_lst,fishbac_coordinates=None, nbpoints=None):
    """
    distributes points and normal vectors on the upper and lower part of 
    the airfoil. Subsequently those points are transformed to the blade 
    reference frame.
    
    
    Parameters
    ----------
    dist_curvature : float
        used as a measure of getting points on a spline if given curvature 
        is exceeded
    
    surfaces_lst : list
        a list of surface names over which the discretization is needed
        
    nbpoints : int
        number of points to be distributed equidistant on a spline,
        used only for tip surfaces since even number of points are desired 
        to form a grid and resolution is not big concern there

    Returns
    -------
    
    """
    if fishbac_coordinates is not None:
        data = fishbac_coordinates
    else:
        data = self.coordinates
    le_idx = np.argmin(np.linalg.norm(data, axis=1)) #not sure if this works for more than one airfoil sections over the blade span

    if 'upper+lower surface' in surfaces_lst:
        data_dict ={'upper+lower surface': data}
    elif 'upper surface' and 'lower surface' in surfaces_lst:
        data_dict={'upper surface':data[0:le_idx+1],'lower surface': data[le_idx:-1]}
    
    # when the end surfaces are being discretized
    if nbpoints:    dist_points={'upper surface':nbpoints,'lower surface': nbpoints,'upper+lower surface': 2*nbpoints}
    
    BSplinelst2d_dict,pnts2d_dict,vecs2d_dict = {},{},{}
    for surf in surfaces_lst:            
        BSplineLst =  BSplineLst_from_dct(data_dict[surf], angular_deflection = 45, closed=False, tol_interp=1e-5, twoD = True)    
        if not nbpoints:
            pnts2d, vecs2d = uniformdeflection_on_BSplineLst(BSplineLst, dist_curvature)    
        else:
            # pnts2d, vecs2d = equidistant_D1_on_BSplineLst(BSplineLst, dist_points[surf])  
            pnts2d, vecs2d = equidistant_D1_on_BSplineLst(BSplineLst, dist_points[surf],surf)  
        BSplinelst2d_dict[surf] = BSplineLst
        pnts2d_dict[surf] = pnts2d
        vecs2d_dict[surf] = vecs2d

    return (BSplinelst2d_dict, pnts2d_dict, vecs2d_dict)
