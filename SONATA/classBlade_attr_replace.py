#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:52:40 2021

@author: Sumeet Kumar
"""
import numpy as np
from scipy.interpolate import interp1d
import time

from OCC.Core.gp import gp_Pnt, gp_Trsf, gp_Ax1, gp_Dir, gp_Pln, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
                        
from SONATA.utl.blade_utl import interp_airfoil_position
from SONATA.cbm.topo.to3d import bsplinelst_to3d, pnt_to3d, vec_to3d
from SONATA.cbm.topo.utils import PntLst_to_npArray
from SONATA.utl.blade_utl import make_loft
from SONATA.cbm.display.display_utils import display_config, display_Ax2, display_cbm_SegmentLst

def trsf_af_to_blfr_disp(loc, pa_loc, chord, twist, deformation_t, rotate, solver = 'CII'):
    Trsf = gp_Trsf()

    trsf_rot1 = gp_Trsf()
    trsf_rot2 = gp_Trsf()
    trsf_rot3 = gp_Trsf()
    trsf_trans1 = gp_Trsf()
    trsf_scale = gp_Trsf()

    trsf_rot1.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,0,1)), -twist)       
    trsf_trans1.SetTranslation(gp_Pnt(pa_loc,0,0), gp_Pnt(0,0,0))
    trsf_scale.SetScale(gp_Pnt(0,0,0), chord)
    trsf_rot2.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), -rotate*np.pi/2)
    trsf_rot3.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,1,0)), -rotate*np.pi/2)


    # if elastic deformation provided then use it to obtain final configuration 
    # of one blade section (airfoil)
    if deformation_t is not None and deformation_t.any(): 
        
        trsf_rot1_deform = gp_Trsf()
        trsf_rot2_deform = gp_Trsf()
        trsf_rot3_deform = gp_Trsf()
        trsf_trans_deform = gp_Trsf()
        
        if solver == 'CII':        
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
        elif solver == 'Dymore':
            trsf_rot1_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(1,0,0)), deformation_t[5]*np.pi/180)
            trsf_rot2_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,1,0)), deformation_t[4]*np.pi/180)        
            trsf_rot3_deform.SetRotation(gp_Ax1(gp_Pnt(pa_loc,0,0), gp_Dir(0,0,1)), deformation_t[3]*np.pi/180)        
            # Dymore to SONATA frame translation conversion 
            trsf_trans_deform.SetTranslation(gp_Pnt(0,0,0), gp_Pnt(loc[0]+deformation_t[0],
                                                                    loc[1]+deformation_t[1],
                                                                    loc[2]+deformation_t[2]))                  
            
            Trsf.Multiply(trsf_trans_deform)
            Trsf.Multiply(trsf_rot3)
            Trsf.Multiply(trsf_rot2)
            Trsf.Multiply(trsf_rot1_deform)
            Trsf.Multiply(trsf_rot2_deform)
            Trsf.Multiply(trsf_rot3_deform)
            Trsf.Multiply(trsf_scale)
            Trsf.Multiply(trsf_trans1)
            Trsf.Multiply(trsf_rot1)
        else:
            #read about error handling and raise error here that for the new solver deformation mapping needs to be carried out
            pass

        
    # simply construct the baseline rotor blade   
    else: 
        
        trsf_trans2 = gp_Trsf()
        #move airfoil sonata coordinate system origin to given spanwise location 
        trsf_trans2.SetTranslation(gp_Pnt(0,0,0), gp_Pnt(loc[0],loc[1],loc[2]))

        #applying the transformations to the blade section of the baseline blade
        #chronologically they get applied bottom first        
        Trsf.Multiply(trsf_trans2)
        Trsf.Multiply(trsf_rot3)
        Trsf.Multiply(trsf_rot2)
        Trsf.Multiply(trsf_scale)
        Trsf.Multiply(trsf_trans1)
        Trsf.Multiply(trsf_rot1)               



def trsf_af_to_blfr_pos(pa_loc, chord, twist, pos_t, rotate, solver = 'Dymore'):
    """
    Can only plot position data output from Dymore right now.
    plotting LL position in inertial frame (EULER_321)

    Parameters
    ----------
    pa_loc : TYPE
        DESCRIPTION.
    chord : TYPE
        DESCRIPTION.
    twist : TYPE
        DESCRIPTION.
    pos_t : TYPE, optional
        DESCRIPTION. The default is None.
    rotate : TYPE, optional
        DESCRIPTION. The default is 1.
    solver : TYPE, optional
        DESCRIPTION. The default is 'Dymore'.

    Returns
    -------
    None.

    """
    Trsf = gp_Trsf()

    trsf_rot1 = gp_Trsf()
    trsf_rot2 = gp_Trsf()
    trsf_rot3 = gp_Trsf()
    trsf_trans1 = gp_Trsf()
    trsf_scale = gp_Trsf()

    #transformation that gets the blade section in Dymore airfoil frame
    #axes orientation also matches
    trsf_trans1.SetTranslation(gp_Pnt(pa_loc,0,0), gp_Pnt(0,0,0))
    trsf_scale.SetScale(gp_Pnt(0,0,0), chord)
    trsf_rot2.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), -rotate*np.pi/2)
    trsf_rot3.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,1,0)), -rotate*np.pi/2)

        
    trsf_rot1_deform = gp_Trsf()
    trsf_rot2_deform = gp_Trsf()
    trsf_rot3_deform = gp_Trsf()
    trsf_rotx_deform = gp_Trsf()
    trsf_roty_deform = gp_Trsf()
    trsf_rotz_deform = gp_Trsf()
    trsf_trans_deform = gp_Trsf()
    
    
    #Dymore airfoil frame to Inertial (EULER_321)      
    trsf_rotx_deform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(1,0,0)), pos_t[5]*np.pi/180)  
    trsf_roty_deform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,1,0)), pos_t[4]*np.pi/180)        
    trsf_rotz_deform.SetRotation(gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1)), pos_t[3]*np.pi/180)        

    #Dymore to SONATA frame translation conversion 
    trsf_trans_deform.SetTranslation(gp_Pnt(0,0,0), gp_Pnt(pos_t[0],         
                                                           pos_t[1],
                                                           pos_t[2]))                  
    
    Trsf.Multiply(trsf_trans_deform)
    # Trsf.Multiply(trsf_rotx_deform) #EULER_321 data in *.mdt for inertial to blade frame transformation
    Trsf.Multiply(trsf_rotz_deform) #so applying angle transformations in reverse to go from airfoil
    Trsf.Multiply(trsf_roty_deform) #to Dymore inertial frame
    Trsf.Multiply(trsf_rotx_deform)
    Trsf.Multiply(trsf_rot3)
    Trsf.Multiply(trsf_rot2)
    Trsf.Multiply(trsf_scale)
    Trsf.Multiply(trsf_trans1) #move origin to where LL is
    # Trsf.Multiply(trsf_rot1) #structural pre-twist is already there in the position data

    return Trsf



def trsf_af_to_blfr(loc, pa_loc, chord, twist, deformation_pos_t, disp_or_pos, rotate, solver = 'CII'):
    """
    Defines the transformation of the airfoil section in 3D space to the blade reference frame location
    and pitch-axis location, scales it with chord and rotates it with given 
    structural twist. Note blade precone value is not needed since blade is 
    being constructed in a frame that is attached to the blade and rotated by
    the precone angle
    If no deformation data provided then simply constructs the baseline blade.
    
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
        blade structural pre-twist
    deformation_t : array, default None
        [xnew,ynew,znew,phi,theta,psi] of airfoil orientation at reference 
        locations loc. If deformation is zero array or None then blade is rigid.
    rotate : int, default 1
        expects 1 or -1 based on CCW or CW rotation direction (rotor viewed from top)
    solver: str, default 'Dymore'
        str to indicate the comprehensive analysis solver used to generate the
        elastic blade bending data. In CII the (in-built) convention is y-axis 
        along blade span and x-axis toward TE (for CCW rotation). In Dymore, the 
        framework has been set up to conform to SONATA coordinates so that 
        x-axis is along blade span and y-axis is towards LE. 
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
    
    if disp_or_pos == 'disp':
        Trsf = trsf_af_to_blfr_disp(loc, pa_loc, chord, twist, deformation_pos_t, rotate, solver = 'CII')
    elif disp_or_pos == 'pos':
        Trsf = trsf_af_to_blfr_pos(pa_loc, chord, twist, deformation_pos_t, rotate, solver = 'Dymore')
        

    return Trsf

def blade_gen_wopwop_mesh(self, radial_res, surfaces_dict, deformation, 
                          nbpoints, dist_curvature=0.0001, fishbac_spantr=0.02, 
                          active_section=[], rotate=1, fishbac_coordinates=None,
                          minset=True, solver = 'CII', disp_or_pos = 'disp'):
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
        to form a grid and resolution is not big concern there. 
    
    dist_curvature : float, optional
        used as a measure of getting points on a spline if given curvature 
        is exceeded. Results in chordwise discretization on lifting 
        surfaces. Default value is 0.0001. This is a legacy feature and not 
        really used for blade surface discretization for now (primarily 
        nbpoints is used).   
        
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
        new radial resolution `radial_newres` is returned.
        
    Returns
    -------
    radial_newres : list
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
    print('radial_res =',list(radial_res))
    if minset:  #not sure if this is handling disp_or_pos = 'pos' data right
        minx = self.blade_ref_axis[:,0]
        morphing_section = []
        if active_section: 
            if active_section[0]-fishbac_spantr>0.0:
                inner_edge = active_section[0]-fishbac_spantr
            else:
                inner_edge = active_section[0]
            if active_section[1]+fishbac_spantr<1.0:
                outer_edge = active_section[1]+fishbac_spantr
            else:
                outer_edge = active_section[1]
            morphing_section = [inner_edge, outer_edge]
        stacked_arr = np.hstack((radial_res,minx,morphing_section,active_section))
        sort_arr = np.sort(stacked_arr)
        # radial_newres = np.unique(sort_arr.round(4))
        radial_newres = np.unique(sort_arr)
        print('radial_newres =',list(radial_newres))
        time.sleep(2)
        deformation_newres = np.zeros((deformation.shape[0],deformation.shape[1],radial_newres.shape[0]))
        for i in range(deformation.shape[0]):
            f_deform_interp = interp1d(radial_res,deformation[i,:,:],kind='cubic', axis=1)        
            deformation_newres[i,:,:] = f_deform_interp(radial_newres)
    
    # if np.array_equal(deformation_newres,deformation): print('they are equal!!!')
    # radial_newres = radial_res
    # deformation_newres = deformation
    print('radial_newres =',list(radial_newres))
    
    
    
    
    
    
    
    
    
    #Start constructing the baseline blade configuration in SONATA (x along span)
    # getting the 2D airfoil data at blade spanwise discretization locations
    airfoil_position = (list(self.airfoils[:,0]),[af.name for af in self.airfoils[:,1]])
    airfoils = list(self.airfoils[:,1])
    wopafls = np.asarray([[x, interp_airfoil_position(airfoil_position, airfoils, x)] for x in radial_newres])    
    
    # iterating through the deformation at different time steps to obtain nodes and normal at each time step
    for time_idx,deformation_t in enumerate(deformation_newres):
        # initializing dictionaries of bsplines, node points 
        # and normals to store corresponding values
        self.wopwop_bsplinelst, self.wopwop_pnts, self.wopwop_vecs = {}, {}, {}
        for surf in surfaces_dict['lifting_surfaces']:
            self.wopwop_bsplinelst[surf], self.wopwop_pnts[surf], self.wopwop_vecs[surf] = [], [], []
        for surf in surfaces_dict['end_surfaces']:
            self.wopwop_bsplinelst[surf], self.wopwop_pnts[surf], self.wopwop_vecs[surf] = [], [], []
        
        # iterating through the span stations to get the nodes and normals at each station
        # discretizing the lifting_surfaces at different radial spans (including the blade tips) and getting the nodes and normals there 
        for station_idx,(x,af) in enumerate(wopafls):
            lift_surf_lst = surfaces_dict['lifting_surfaces']
    
            if x==radial_newres[0] or x==radial_newres[-1]:    # repeating code below, not the most efficient but does the job for now
                (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                                   lift_surf_lst,
                                                                                   nbpoints=nbpoints)    

                if active_section:
                    if x==active_section[0]: 
                        (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                       lift_surf_lst,
                                                                       fishbac_coordinates=fishbac_coordinates[:,:,time_idx],
                                                                       nbpoints=nbpoints)
                    if x==active_section[-1]:
                        (BSplineLst2d_dict, pnts2d_dict, vecs2d_dict) = af.gen_wopwop_dist(dist_curvature,
                                                                       lift_surf_lst,
                                                                       fishbac_coordinates=fishbac_coordinates[:,:,time_idx],
                                                                       nbpoints=nbpoints)                      

            
                for surf in BSplineLst2d_dict:                
                    
                    BSplineLst2d = BSplineLst2d_dict[surf]
                    pnts2d = pnts2d_dict[surf]
                    vecs2d = vecs2d_dict[surf]
                    Pnts = [pnt_to3d(p) for p in pnts2d]
                    Vecs = [vec_to3d(v) for v in vecs2d]
                    BSplineLst = bsplinelst_to3d(BSplineLst2d, gp_Pln(gp_Pnt(0,0,0), gp_Dir(0,0,1)))
                    Trsf = trsf_af_to_blfr(self.f_blade_ref_axis.interpolate(x)[0][0], 
                                           float(self.f_ta(x)), float(self.f_chord(x)),
                                           float(self.f_twist(x)), 
                                           deformation_t[:,station_idx], 
                                           disp_or_pos,
                                           rotate,
                                           solver = solver)
                    [s.Transform(Trsf) for s in BSplineLst]  #what is this doing??
                    Pnts = [p.Transformed(Trsf) for p in Pnts]
                    Vecs = [v.Transformed(Trsf) for v in Vecs]                
                    Vecs_norm = [v.Normalized() for v in Vecs]
                    
    
                    # Nodes at the tip surfaces will be same as lifting surface there. Getting also the normals only for completeness. 
                    # Normals at end_surfaces not obtained using wopwop_vecs. They are calculated separately, see below. 
    
                    if x==radial_newres[0]:    
                        end_surf='inboard tip'
                    else:
                        end_surf='outboard tip'
                        
                    if surf=='upper+lower surface':
                        if end_surf in surfaces_dict['end_surfaces']:
                            self.wopwop_pnts[end_surf].append(Pnts)
                            self.wopwop_vecs[end_surf].append(Vecs)
                    elif surf=='upper surface':  
                        if end_surf in surfaces_dict['end_surfaces']:
                            self.wopwop_pnts[end_surf].append(Pnts)
                            self.wopwop_vecs[end_surf].append(Vecs)
                    elif surf=='lower surface':    #to have the results in the same order as in WOPWOP Case4 example
                        Pnts.reverse()
                        Vecs.reverse()
                        if end_surf in surfaces_dict['end_surfaces']:
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
                Trsf = trsf_af_to_blfr(self.f_blade_ref_axis.interpolate(x)[0][0], 
                                       float(self.f_ta(x)), float(self.f_chord(x)),
                                       float(self.f_twist(x)), 
                                       deformation_t[:,station_idx], 
                                       disp_or_pos,
                                       rotate,
                                       solver = solver)
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
            if solver=='CII':
                tmp_arr1 = np.transpose(deformation_t[0:3,:])
                tmp_arr2 = np.zeros_like(tmp_arr1)
                tmp_arr2[:,0] = tmp_arr1[:,1]
                tmp_arr2[:,1] = -tmp_arr1[:,0]
                tmp_arr2[:,2] = tmp_arr1[:,2]    
                compact_patchnode_arr_3d = np.expand_dims(tmp_arr2,axis=1)
                compact_patchnorm_arr_3d = np.zeros_like(compact_patchnode_arr_3d)
            elif solver=='Dymore': #in Dymore model construction it is made sure apriori that the frame
                deformation_t_tr = np.transpose(deformation_t[0:3,:])
                compact_patchnode_arr_3d = np.expand_dims(deformation_t_tr,axis=1)
                compact_patchnorm_arr_3d = np.zeros_like(compact_patchnode_arr_3d)
                
        else:
            compact_patchnode_arr_2d=self.f_blade_ref_axis.interpolate(radial_newres)[0]          # the lifting-line is at the location of 'Reference axis' in *.yml file. Interpolated to the spanwise discretization of blade
            compact_patchnode_arr_3d = np.expand_dims(compact_patchnode_arr_2d,axis=1)
            # node_pos_arr_dict_t[compact_surf]=compact_patchnode_arr_3d
        
        node_pos_arr_dict_t[compact_surf]=compact_patchnode_arr_3d
        norm_pos_arr_dict_t[compact_surf]=compact_patchnorm_arr_3d
            
        # correcting the normals at the end patches to be unit normals along x-axis (in SONATA coordinates)
        # This is needed since wopwop_vecs[end_surf] is essentially normal to the lifting surface spline and not the tip surface which is what's required
        for end_surf in surfaces_dict['end_surfaces']:                             #Converting normals on end_surfaces to unit normals 
            v1 = norm_pos_arr_dict_t['upper surface'][0,0,:]
            v2 = norm_pos_arr_dict_t['lower surface'][0,0,:]
            v3 = np.cross(v1,v2)
            v3 = v3/np.linalg.norm(v3)    #end surfaces are perpendicular to the wrapping surfaces
            shp = np.shape(norm_pos_arr_dict_t[end_surf])
            if 'inboard' in end_surf:
                norm_pos_arr_dict_t[end_surf] =  np.tile(v3,(shp[0],shp[1],1))
            else:
                norm_pos_arr_dict_t[end_surf] =  np.tile(-v3,(shp[0],shp[1],1))

        if time_idx==0:
            node_pos_arr_dict, norm_pos_arr_dict = {}, {}
            for surf in node_pos_arr_dict_t:
                node_pos_arr_dict[surf] = np.zeros(node_pos_arr_dict_t[surf].shape+deformation_newres[:,0,0].shape)
                norm_pos_arr_dict[surf] = np.zeros(norm_pos_arr_dict_t[surf].shape+deformation_newres[:,0,0].shape)
        # print(np.shape(deformation_newres))
        # for surf in node_pos_arr_dict_t: 
        #     node_pos_arr_dict[surf][:,:,:,time_idx] = node_pos_arr_dict_t[surf]
        #     norm_pos_arr_dict[surf][:,:,:,time_idx] = norm_pos_arr_dict_t[surf]

        if time_idx!=deformation_newres.shape[0]-1:                
            for surf in node_pos_arr_dict_t: 
                node_pos_arr_dict[surf][:,:,:,time_idx] = node_pos_arr_dict_t[surf]
                norm_pos_arr_dict[surf][:,:,:,time_idx] = norm_pos_arr_dict_t[surf]
            if time_idx==0:    #making sure data is periodic
                for surf in node_pos_arr_dict_t: 
                    node_pos_arr_dict[surf][:,:,:,deformation_newres.shape[0]-1] = node_pos_arr_dict_t[surf]
                    norm_pos_arr_dict[surf][:,:,:,deformation_newres.shape[0]-1] = norm_pos_arr_dict_t[surf]

    return radial_newres, node_pos_arr_dict, norm_pos_arr_dict                                    

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
