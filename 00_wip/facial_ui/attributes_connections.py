'''
Created on 27 nov. 2014

@author: gamma project
'''

import os, sys

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from SmartRig.UI_hideJoint import Ui_Dialog as UI
from pprint import pprint


bsNode = pm.ls('vic_blendshape:blendShapeBody', r = 1)
# get blendshape target
for bs in bsNode:
    res = pm.aliasAttr(bs, q= True)

    for elt in res:
        if elt.startswith('L_e_'):
#             L_eyeLid_ctrl = pm.ls('L_eyeLid_ctrl')[0]
            # create attribute
#             try:
#                 pm.addAttr(L_eyeLid_ctrl, L_eyeLid_ctrl = elt, min = 0, max = 1, dv = 0)
#                 ctrlAttr = '%s.%s' % (L_eyeLid_ctrl.name(),elt)
#                 pm.setAttr(ctrlAttr, keyable = True)
#             except Exception as ex:
#                 print ex
            print('L_eyeLid_ctrl', elt)
            # connection
            
        elif elt.startswith('R_e_'):
#             print'R_eyeLid_ctrl'
            print('R_eyeLid_ctrl', elt)
        elif elt.startswith('L_eb_'):
#             print'L_eyeBrow_ctrl'
            print('L_eyeBrow_ctrl', elt)
        elif elt.startswith('R_eb_'):
#             print'R_eyeBrow_ctrl'
            print('R_eyeBrow_ctrl', elt)
        elif elt.startswith('M_m_') or elt.startswith('L_m_') or elt.startswith('R_m_'):
#             print'M_mouth_ctrl'
            print('M_mouth_ctrl', elt)
        else:
            pass
            
        
# find controller matching
# create attribute
# connect attributes

# clear controllers attributes
# test = pm.ls(sl = True)[0]
# res = test.listAttr(visible = True, keyable = True, connectable  = True)
# pprint(res)
