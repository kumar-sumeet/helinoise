#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 17:37:40 2022

@author: ge56beh
"""
import numpy as np
import copy

def runsetup(wopwop_datapath,periodicOraperiodic):

    mdls =  [
            'hartii',
            'bo105_simple',
            'bo105_simple_fromhartii',
            'bo105_simple_fromhartiiquicktrim',
            'bo105_complex',
            'uh60a',
            'test',
            'wing',
            'wing',
            'wing',
            'wingCOARSE',
            'utaustin_2bladedstacked',
            'utaustin_4bladedstacked',
            'utaustin_stacked',
            'utaustin_2bladedccr',
            'utaustin_4bladedccr',
            'utaustin_ccr',
             ]
    
    SONATA_ymlfilepaths = [
                            './SONATA/hartii.yml',
                                                                './SONATA/bo105.yml',
                                                                './SONATA/bo105.yml',
                                                                './SONATA/bo105.yml',
                            './SONATA/bo105.yml',
                                                                './SONATA/uh60atest.yml',
                                                                './SONATA/bo105.yml',
                            './SONATA/wing_rectangularAnsellAR5.yml',                       
                            './SONATA/wing_elliptical.yml',                       
                            './SONATA/wing_rectangular.yml',                       
                                                                './SONATA/wing_rectangular.yml',                       
                            './SONATA/UTAustin_stacked.yml',                       
                            './SONATA/UTAustin_stacked.yml',                       
                            './SONATA/UTAustin_stacked.yml',                       
                            './SONATA/UTAustin_ccr.yml',                       
                            './SONATA/UTAustin_ccr.yml',                       
                            './SONATA/UTAustin_ccr.yml',                       
                          ]
    
    #make sure both loading and position data is available in the given dataframename
    # ['DymInertial', 'WopwopInertial', 'Rotor(non-rotating)', 'Rotor(rotating)', 'BladeHub(rotating)', 'BladePrecone(rotating)']
    dataframenamess = [
                        ['DymInertial','BladePrecone(rotating)'],
                                                                ['DymInertial','BladePrecone(rotating)'], 
                                                                ['BladePrecone(rotating)','DymInertial','WopwopInertial'],
                                                                ['BladePrecone(rotating)','DymInertial','WopwopInertial'],
                        ['DymInertial','BladePrecone(rotating)'],
                                                                ['DymInertial','BladePrecone(rotating)'],
                                                                ['DymInertial','BladePrecone(rotating)'],
                        ['DymInertial','Wing(non-pitching)','Wing(pitching)'],
                        ['DymInertial','Wing(non-pitching)','Wing(pitching)'],
                        ['DymInertial','Wing(non-pitching)','Wing(pitching)'],
                                                                ['DymInertial','Wing(non-pitching)','Wing(pitching)'],
                        ['DymInertial'],#'BladePrecone(rotating)-R1',
                        ['DymInertial'],
                        ['DymInertial'],
                        ['DymInertial'],
                        ['DymInertial'],
                        ['DymInertial'],
                     ]

    filenamess = [  [#hartii
                    ],
                  
                                                                    [#bo105_simple
                                                                    ],
                                                
                                                
                                                                    [#bo105_simple_fromhartii
                                                                    ],
                                                
                                                                    [#bo105_simple_fromhartiiquicktrim
                                                                    ],
                    
                    [#bo105_complex
                     '1994_Run42_7_baseline_trimwithrcvs',
                     ],
                    
                                                                                [#uh60a                                                             
                                                                                ],                        
                                                                                    

                                                                                [#test
                                                                                ],

                    [#wing   ->   wingAnsell
                    ],

                    [#wingelliptical
                    ],      

                    [#wing2D
                    ],      

                                                                        [#wingCOARSE
                                                                        ],
                    
                    [#utaustin_2bladedstacked
                    ],                        
                    [#utaustin_4bladedstacked
                    ],                        
                    [#utaustin_stacked
                    ],                        
                    [#utaustin_2bladedccr
                    ],                        
                    [#utaustin_4bladedccr
                    ],                        
                    [#utaustin_ccr
                    ],                        
                ]

    wopwopoutdirss = [
                           [#hartii
                            ],
                            [#bo105_simple
                            ],
                           [#bo105_simple_fromhartii
                            ],
                           [#bo105_simple_fromhartiiquicktrim
                            ],
                           [#bo105_complex
                            f'{wopwop_datapath}',
                            ],
                           [#uh60a
                            ],
                           [#test
                            ],
                           [#wingAnsell
                            ],
                           [#wing
                            ],
                           [#wing
                            ],
                           [#wingCOARSE
                            ],                           
                            [#utaustin_2bladedstacked
                            ],                        
                            [#utaustin_4bladedstacked
                            ],                        
                            [#utaustin_stacked
                            ],                        
                            [#utaustin_2bladedccr
                            ],                        
                            [#utaustin_4bladedccr
                            ],                        
                            [#utaustin_ccr
                            ],                        
                         ]


    return mdls, SONATA_ymlfilepaths, dataframenamess, filenamess, wopwopoutdirss

