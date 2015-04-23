'''
Created on 9 dec. 2014

@author: gamma project
'''
import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from pprint import pprint

import re


headSquash = pm.PyNode('head_squash_Handle')
bendHeadRL = pm.PyNode('bend_headRL_Handle')
bendHeadFB = pm.PyNode('bend_headFB_Handle')


headGrp = ['body_grp','m_eye_geo_group', 'eye_patch_grp' ]

pm.nonLinear(headSquash, e = True, g = headGrp )
pm.nonLinear(bendHeadRL, e = True, g = headGrp )
pm.nonLinear(bendHeadFB, e = True, g = headGrp )


helmetSquash = pm.PyNode('helmet_squash_Handle')
bendHelmetRL = pm.PyNode('bend_helmetFB_Handle')
bendHelmetFB = pm.PyNode('bend_helmetRL_Handle')


helmetGrp = ['helmet_grp']

pm.nonLinear(helmetSquash, e = True, g = helmetGrp )
pm.nonLinear(bendHelmetRL, e = True, g = helmetGrp )
pm.nonLinear(bendHelmetFB, e = True, g = helmetGrp )



# test = pm.ls(sl = True)
# print(test)
# pm.select(test)
# 
# newSel = []
# for elt in test:
#     newSel.append(elt.replace('halvar_facial:','')) 
#     
# pm.select(newSel)


