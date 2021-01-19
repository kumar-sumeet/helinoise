#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:52:40 2021

@author: Sumeet Kumar
"""
import numpy as np
from scipy.interpolate import interp1d

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Ax1, gp_Dir, gp_Pln, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
                        
from SONATA.utl.blade_utl import interp_airfoil_position
from SONATA.cbm.topo.to3d import bsplinelst_to3d, pnt_to3d, vec_to3d
from SONATA.cbm.topo.utils import PntLst_to_npArray
from SONATA.utl.blade_utl import make_loft
from SONATA.cbm.display.display_utils import display_config, display_Ax2, display_cbm_SegmentLst

def trsf_af_to_blfr(loc, pa_loc, chord, twist, deformation_t=None, rotate =1):
    """
    Defines the transformation in 3D space to the blade reference frame location
    and pitch-axis location, scales it with chord and rotates it with 'twist'
    
    Parameters
    ----------
    loc : array
        [x,y,z] position in blade reference coordinates
    pa_loc : float
        nondim. pitch axis location
    chord : float
        chord length
    twist : float
        twist angle about x in radians
    deformation_t : array
        [xnew,ynew,znew,phi,theta,psi] of airfoil orientation at reference 
        locations loc. If deformation is zero array or None then blade is rigid.
    
    Returns
    ---------
    Trsf : OCC.gp_Trsf 
        non-persistent transformation in 3D space.
        
    Todo 
    --------- 
    implement to transfer to the deformed stated, check for rotational definition!
        [xnew,ynew,znew,phi,theta,psi] deformation vector is defined as...
            
    """
   
    Trsf = gp_Trsf()

    trsf_rot1 = gp_Trsf()
    trsf_rot2 = gp_Trsf()
    trsf_rot3 = gp_Trsf()
    trsf_trans1 = gp_Trsf()
    trsf_scale = gp_Trsf()

    trsf_rot1.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,0,1)), -twist)    # blade structural pre-twist    
    trsf_trans1.SetTranslation(gp_Pnt(pa_loc,0,0), gp_Pnt(0,0,0))
    trsf_scale.SetScale(gp_Pnt(0,0,0), chord)
    trsf_rot2.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), -rotate*np.pi/2)
    trsf_rot3.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,1,0)), -rotate*np.pi/2)

    if deformation_t is not None and deformation_t.any(): 
        
        trsf_rot1_deform = gp_Trsf()
        trsf_rot2_deform = gp_Trsf()
        trsf_rot3_deform = gp_Trsf()
        trsf_trans_deform = gp_Trsf()
                
        # Euler angles XYZ rotations provided in CII output implemented in SONATA
        trsf_rot1_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,1,0)), deformation_t[5])
        trsf_rot2_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,0,1)),-deformation_t[4])        
        trsf_rot3_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(1,0,0)), deformation_t[3])        
        # CII to SONATA frame translation conversion 
        trsf_trans_deform.SetTranslation(gp_Pnt(0,0,0), gp_Pnt(deformation_t[1],-deformation_t[0],deformation_t[2]))      
        
        Trsf.Multiply(trsf_trans_deform)
        Trsf.Multiply(trsf_rot3)
        Trsf.Multiply(trsf_rot2)
        Trsf.Multiply(trsf_scale)
        Trsf.Multiply(trsf_trans1)
        Trsf.Multiply(trsf_rot1_deform)
        Trsf.Multiply(trsf_rot2_deform)
        Trsf.Multiply(trsf_rot3_deform)
        Trsf.Multiply(trsf_rot1)
        
    else:
        
        trsf_trans2 = gp_Trsf()
        
        trsf_trans2.SetTranslation(gp_Pnt(0,0,0), gp_Pnt(loc[0],loc[1],loc[2]))
        
        Trsf.Multiply(trsf_trans2)
        Trsf.Multiply(trsf_rot3)
        Trsf.Multiply(trsf_rot2)
        Trsf.Multiply(trsf_scale)
        Trsf.Multiply(trsf_trans1)
        Trsf.Multiply(trsf_rot1)

    return Trsf

def blade_gen_wopwop_mesh(self, radial_res, surfaces_dict, deformation, 
                          nbpoints=50, dist_curvature=0.0001, fishbac_spantr=0.02, 
                          active_section=[], rotate=1, fishbac_coordinates=None,
                          minset=True):
    """
    Blade method to generate a discretization of the blade lifting surface that
    is necessary for acoustic analysis. Structured mesh of nodes and 
    corresponding normals is generated. The normals are currently only 
    impemented such that they are within the crosssectional plane 
    (normals = '2d') and therefore won't be strictly normal to the surface if 
    the section airfoil over the blade span or the chord length changes. 
    
    Parameters
    ----------
    radial_res : array 
        radial resolution in the form of an array that specifies the radial 
        locations for discretization
            
    surfaces_dict : dict
        dictionary categorizing the different patch names for which the 
        nodes and normals data is required 
    
    deformation : array
        in the futur it shall be possible pass a deformation vector of 3 
        displacements and 3 rotations to get the mesh of the deformed 
        rotor-blade. This function is carried out in the trsf_af_to_blfr
    
    nbpoints : int, optional
        number of points to be distributed equidistant on a spline,
        used only for tip surfaces since even number of points are desired 
        to form a grid and resolution is not big concern there. Default is 50.
    
    dist_curvature : float, optional
        used as a measure of getting points on a spline if given curvature 
        is exceeded. Results in chordwise discretization on lifting 
        surfaces. Default value is 0.0001.
        
    fishbac_spantr : float, optional
        spanwise active camber morphing transition regios as a fraction of 
        blade radius. Default value is 0.02.    
    
    active_section : list, optional
        non-dimensional blade span locations indicating the beginning and 
        end of active morphing section. Default value is an empty list, 
        signifying a non-morphing blade.
    
    rotate : int, optional
        rotation direction of the rotor. 1 is counter-clockwise, 0 is clockwise

    fishbac_coordinates : array, optional
        TEF deflection (in units used in CII run) at every time step. None 
        if no morphing occurs throughout the blade span
        
    minset : bool, optional
        if true the minimum set of radial values (where transitional 
        properties occur) are superimposed with the radial_res array and the 
        new radial resolution `radial_res_new` is returned.
        
    Returns
    -------
    radial_res_new : list
        the new radial discretization that includes the prescribed radial
        discretization  `radial_res` as well as any stations where transition 
        of properties occurs based on `*.yml` file input. 
    node_pos_arr_dict : dict
        keys are the patch names in surfaces_dict and the values are the 
        corresponding node point coordinates in SONATA coordinates
    norm_pos_arr_dict :  dict
        keys are the patch names in surfaces_dict and the values are the 
        corresponding unit normal vectors in SONATA coordinates
        
    """
    if minset:
        minx = self.blade_ref_axis[:,0]
        morphing_section = []
        if active_section: 
            morphing_section = [active_section[0]-fishbac_spantr, active_section[1]+fishbac_spantr]
        radial_res_new = np.unique(np.sort(np.hstack((radial_res,minx,morphing_section,active_section))))
        deformation_new_res = np.zeros((deformation.shape[0],deformation.shape[1],radial_res_new.shape[0]))
        for i in range(deformation.shape[0]):
            f_deform_interp = interp1d(radial_res,deformation[i,:,:],kind='cubic', axis=1)        
            deformation_new_res[i,:,:] = f_deform_interp(radial_res_new)
    
    if np.array_equal(deformation_new_res,deformation): print('they are equal!!!')
    # getting the airfoil data at blade spanwise discretization locations
    airfoil_position = (list(self.airfoils[:,0]),[af.name for af in self.airfoils[:,1]])
    airfoils = list(self.airfoils[:,1])
    wopafls = np.asarray([[x, interp_airfoil_position(airfoil_position, airfoils, x)] for x in radial_res_new])        
    # iterating through the deformation at different time steps to obtain nodes and normal at each time step
    for time_idx,deformation_t in enumerate(deformation_new_res):
        # initializing dictionaries of bsplines, node points and normals to store corresponding values
        self.wopwop_bsplinelst, self.wopwop_pnts, self.wopwop_vecs = {}, {}, {}
        for surf in surfaces_dict['lifting_surfaces']:
            self.wopwop_bsplinelst[surf], self.wopwop_pnts[surf], self.wopwop_vecs[surf] = [], [], []
        for surf in surfaces_dict['end_surfaces']:
            self.wopwop_bsplinelst[surf], self.wopwop_pnts[surf], self.wopwop_vecs[surf] = [], [], []
        
        # iterating through the span stations to get the nodes and normals at each station
        # discretizing the lifting_surfaces at different radial spans (including the blade tips) and getting the nodes and normals there 
    
        for station_idx,(x,af) in enumerate(wopafls):
            lift_surf_lst = surfaces_dict['lifting_surfaces']
    
            if x==radial_res_new[0] or x==radial_res_new[-1]:    # repeating code below, not the most efficient but does the job for now
                (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                                   lift_surf_lst,
                                                                                   nbpoints=nbpoints)    
                for surf in BSplineLst2d_dict:                
                    
                    BSplineLst2d = BSplineLst2d_dict[surf]
                    pnts2d = pnts2d_dict[surf]
                    vecs2d = vecs2d_dict[surf]
                    Pnts = [pnt_to3d(p) for p in pnts2d]
                    Vecs = [vec_to3d(v) for v in vecs2d]
                    BSplineLst = bsplinelst_to3d(BSplineLst2d, gp_Pln(gp_Pnt(0,0,0), gp_Dir(0,0,1)))
                    Trsf = trsf_af_to_blfr(self.f_blade_ref_axis.interpolate(x)[0][0], float(self.f_ta(x)), float(self.f_chord(x)), float(self.f_twist(x)), deformation_t[:,station_idx], rotate = rotate)
                    [s.Transform(Trsf) for s in BSplineLst]
                    Pnts = [p.Transformed(Trsf) for p in Pnts]
                    Vecs = [v.Transformed(Trsf) for v in Vecs]                
                    Vecs_norm = [v.Normalized() for v in Vecs]
                    
    
                    # Nodes at the tip surfaces will be same as lifting surface there. Getting also the normals only for completeness. 
                    # Normals at end_surfaces not obtained using wopwop_vecs. They are calculated separately, see below. 
    
                    if x==radial_res_new[0]:    
                        end_surf='inboard tip'
                    else:
                        end_surf='outboard tip'
                        
                    if surf=='upper+lower surface':
                        self.wopwop_pnts[end_surf].append(Pnts)
                        self.wopwop_vecs[end_surf].append(Vecs)
                    elif surf=='upper surface':  
                        self.wopwop_pnts[end_surf].append(Pnts)
                        self.wopwop_vecs[end_surf].append(Vecs)
                    elif surf=='lower surface':    #to have the results in the same order as in WOPWOP Case4 example
                        Pnts.reverse()
                        Vecs.reverse()
                        self.wopwop_pnts[end_surf].append(Pnts)
                        self.wopwop_vecs[end_surf].append(Vecs)
            if active_section and  x>=active_section[0] and x<=active_section[1]: 
                # fishbac section
                (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                                   lift_surf_lst,
                                                                                   fishbac_coordinates=fishbac_coordinates[:,:,time_idx],
                                                                                   nbpoints=nbpoints)
                                                                                       
            else:
                # normal section
                (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                                   lift_surf_lst,
                                                                                   nbpoints=nbpoints)
                                                                                   
            # all sections
            for surf in BSplineLst2d_dict:                
                
                BSplineLst2d = BSplineLst2d_dict[surf]
                pnts2d = pnts2d_dict[surf]
                vecs2d = vecs2d_dict[surf]
                Pnts = [pnt_to3d(p) for p in pnts2d]
                Vecs = [vec_to3d(v) for v in vecs2d]
                BSplineLst = bsplinelst_to3d(BSplineLst2d, gp_Pln(gp_Pnt(0,0,0), gp_Dir(0,0,1)))
                Trsf = trsf_af_to_blfr(self.f_blade_ref_axis.interpolate(x)[0][0], float(self.f_ta(x)), float(self.f_chord(x)), float(self.f_twist(x)), deformation_t[:,station_idx], rotate = rotate)
                [s.Transform(Trsf) for s in BSplineLst]
                Pnts = [p.Transformed(Trsf) for p in Pnts]
                Vecs = [v.Transformed(Trsf) for v in Vecs]                
                Vecs_norm = [v.Normalized() for v in Vecs]
                
                self.wopwop_pnts[surf].append(Pnts)
                self.wopwop_vecs[surf].append(Vecs_norm)
        # writing the node coordinates and normals as arrays into dictionaries with keys being ALL the patch names given in surfaces_dict EXCEPT compact surfaces        
        node_pos_arr_dict_t, norm_pos_arr_dict_t={}, {}
        for (surf,meshpnts), (_,meshvecs) in zip(self.wopwop_pnts.items(),self.wopwop_vecs.items()):            
            norm_pos_arr_dict_t[surf] =  np.asarray([PntLst_to_npArray(cs) for cs in meshvecs])           # normal vectors at the nodes 
            node_pos_arr_dict_t[surf] =  np.asarray([PntLst_to_npArray(cs) for cs in meshpnts])           # node vectors            
        compact_surf = surfaces_dict['compact_surfaces'][0]
        if deformation.any():
            tmp_arr1 = np.transpose(deformation_t[0:3,:])
            tmp_arr2 = np.zeros_like(tmp_arr1)
            tmp_arr2[:,0] = tmp_arr1[:,1]
            tmp_arr2[:,1] = -tmp_arr1[:,0]
            tmp_arr2[:,2] = tmp_arr1[:,2]    
            compact_patch_arr_3d = np.expand_dims(tmp_arr2,axis=1)
        else:
            compact_patch_arr_2d=self.f_blade_ref_axis.interpolate(radial_res_new)[0]          # the lifting-line is at the location of 'Reference axis' in *.yml file. Interpolated to the spanwise discretization of blade
            compact_patch_arr_3d = np.expand_dims(compact_patch_arr_2d,axis=1)
            node_pos_arr_dict_t[compact_surf]=compact_patch_arr_3d
        
        node_pos_arr_dict_t[compact_surf]=compact_patch_arr_3d
        norm_pos_arr_dict_t[compact_surf]=np.zeros_like(compact_patch_arr_3d)
            
        # correcting the normals at the end patches to be unit normals along x-axis (in SONATA coordinates)
        # This is needed since wopwop_vecs[end_surf] is essentially normal to the lifting surface spline and not the tip surface which is what's required
        for end_surf in surfaces_dict['end_surfaces']:                             #Converting normals on end_surfaces to unit normals 
            if 'inboard' in end_surf:
                # this is not exactly right since the blade might have a pre-cone
                # fix it later
                norm_pos_arr_dict_t[end_surf][:,:,0]=-np.ones_like(norm_pos_arr_dict_t[end_surf][:,:,0])
            else:
                # this is not exactly right since the blade might have a pre-cone
                # fix it later
                norm_pos_arr_dict_t[end_surf][:,:,0]=np.ones_like(norm_pos_arr_dict_t[end_surf][:,:,0])
            norm_pos_arr_dict_t[end_surf][:,:,1]=np.zeros_like(norm_pos_arr_dict_t[end_surf][:,:,1])
            norm_pos_arr_dict_t[end_surf][:,:,2]=np.zeros_like(norm_pos_arr_dict_t[end_surf][:,:,2])     
        if time_idx==0:
            node_pos_arr_dict, norm_pos_arr_dict = {}, {}
            for surf in node_pos_arr_dict_t:
                node_pos_arr_dict[surf] = np.zeros(node_pos_arr_dict_t[surf].shape+deformation_new_res[:,0,0].shape)
                norm_pos_arr_dict[surf] = np.zeros(norm_pos_arr_dict_t[surf].shape+deformation_new_res[:,0,0].shape)
        for surf in node_pos_arr_dict_t: 
            node_pos_arr_dict[surf][:,:,:,time_idx] = node_pos_arr_dict_t[surf]
            norm_pos_arr_dict[surf][:,:,:,time_idx] = norm_pos_arr_dict_t[surf]

    return radial_res_new, node_pos_arr_dict, norm_pos_arr_dict                                    

# def blade_post_3dtopo(self, flag_wf = True, flag_lft = False, flag_topo = False, flag_mesh = False, flag_wopwop=False):
#     """
#     generates the wireframe and the loft surface of the blade

#     Returns
#     ----------
#     loft : OCC.TopoDS_surface
#         the 3D surface of the blade
    
#     wireframe : list
#         list of every airfoil_wire scaled and rotated at every grid point
        
        
#     ToDo
#     ----------

#     """
#     (self.display, self.start_display, self.add_menu, self.add_function_to_menu) = display_config(cs_size = 0.5, DeviationAngle = 1e-4, DeviationCoefficient = 1e-4)
    
#     if flag_wf:
#         wireframe = []
        
#         #visualize blade and beam reference axis
#         for s in self.blade_ref_axis_BSplineLst:
#             self.display.DisplayShape(s, color='RED')
        
#         for s in self.beam_ref_axis_BSplineLst:
#             self.display.DisplayShape(s, color='GREEN')
        
#         #airfoil wireframe
#         for bm, afl in zip(self.blade_matrix, self.airfoils[:,1]):
#             (wire, te_pnt) = afl.trsf_to_blfr(bm[1:4], bm[6], bm[4], bm[5])
#             wireframe.append(wire)
#             self.display.DisplayShape(wire, color='BLACK')
#             #self.display.DisplayShape(te_pnt, color='WHITE', transparency=0.7)
            
#     if flag_lft:
#         for i in range(len(wireframe)-1):
#             loft = make_loft(wireframe[i:i+2], ruled=True, tolerance=1e-2, continuity=1, check_compatibility=True)
#             self.display.DisplayShape(loft, transparency=0.5, update=True)
    
#     if flag_topo:
#         for (x,cs) in self.sections:
#             #display sections
#             display_Ax2(self.display, cs.Ax2, length=0.2)
#             display_cbm_SegmentLst(self.display, cs.SegmentLst, self.Ax2, cs.Ax2)
            
#     if flag_wopwop:
#         for surface in self.wopwop_bsplinelst:
#             for bspl in self.wopwop_bsplinelst[surface]:
#                 for s in bspl:
#                     self.display.DisplayShape(s, color='GREEN')
#             tmp_j=0
#             for i,cs in enumerate(self.wopwop_pnts[surface]):
#                 for j,p1 in enumerate(cs):
#                     v2 = self.wopwop_vecs[surface][i][j]
#                     v1 = gp_Vec(p1.XYZ())
#                     if j==0 and tmp_j==0:    print('\n',v2,v2.Coord())
#                     v2.Normalize()
#                     if j==0 and tmp_j==0:    print(v2,v2.Coord())
#                     v2.Multiply(0.1)
#                     if j==0 and tmp_j==0:    
#                         print(v2,v2.Coord())
#                         tmp_j=1
#                     v3 = v1.Added(v2)
#                     p2 = gp_Pnt(v3.XYZ())
                    
#                     self.display.DisplayShape(p1, color='RED')    
#                     h1 = BRepBuilderAPI_MakeEdge(p1,p2).Shape()
#                     self.display.DisplayShape(h1, color='WHITE')     
    
#     self.display.View_Iso()
#     self.display.FitAll()
#     self.start_display()   
#     return None     
