'''
Created on 25 nov. 2014

@author: gamma project
'''


import os, sys

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from SmartRig.UI_hideJoint import Ui_Dialog as UI
from pprint import pprint



def createGroup(newName):
    facCtrlGrp = None
    facTmp =  pm.ls(newName)
    if not len(facTmp)>0:
        facCtrlGrp = pm.group(name = newName, world  = True, empty = True)
    else:
        facCtrlGrp = facTmp[0]
        print('already exists')
    return facCtrlGrp

def createCircle(sel, axis):
#     sel = pm.ls(sl = True)[0]
    print sel
    oneGroup = None
    oneCircle = None
    if not sel.endswith('_end'):
        oneCircle = pm.circle(n = (sel.name().replace('_jnt', '') + "_ctrl"), ch = False, o = True, nr = axis, r =1.5)[0]
        print oneCircle
        oneGroup = pm.group(em = True, name = ( oneCircle.name().replace('_ctrl', '_grp')))
        
        oneCircle.setParent(oneGroup)
        pm.parent(oneGroup, sel, r = True)
        pm.parent(oneGroup, w = True)
        
    return oneGroup, oneCircle


sel = pm.ls(sl = True)
headGrp = createGroup('tongue_ctrls_grp')

for s in sel:
    grpTmp = None
    circTmp = None
    grpTmp, circTmp = createCircle(s, [1,0,0])
    print(grpTmp)
    if grpTmp and circTmp:
        grpTmp.setParent(headGrp)
        pm.parentConstraint(circTmp, s, maintainOffset = False, weight = 1 )
