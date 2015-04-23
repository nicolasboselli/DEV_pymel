'''
Created on 25 nov. 2014

@author: gamma project
'''


import os, sys

# smartRig = r'C:\Users\Gamma Project\Documents\maya\scripts'
# sys.path.append(smartRig)

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from SmartRig.UI_hideJoint import Ui_Dialog as UI
# reload(UI_hideJoint)

from pprint import pprint


def createCircle(sel, axis):
#     sel = pm.ls(sl = True)[0]
    print sel
    oneCircle = pm.circle(n = (sel.name().replace('_jnt', '') + "_ctrl"), ch = False, o = True, nr = axis, r =0.1)[0]
    print oneCircle
    oneGroup = pm.group(em = True, name = ( oneCircle.name().replace('_ctrl', '_grp')))
    
    oneCircle.setParent(oneGroup)
    pm.parent(oneGroup, sel, r = True)
    pm.parent(oneGroup, w = True)
    return oneGroup, oneCircle

allSel = pm.ls(sl= True)
for sel in allSel:
    createCircle(sel, [1,0,0])

def createFacialGrp(newName):
    facCtrlGrp = None
    facTmp =  pm.ls(newName)
    if not len(facTmp)>0:
        facCtrlGrp = pm.group(name = newName, world  = True, empty = True)
    else:
        facCtrlGrp = facTmp[0]
        print('already exists')
    return facCtrlGrp

def createZeroParent(sel):
    oldParent = pm.listRelatives(sel, allParents = True)
    oneGroup = pm.group(em = True, name = ( sel.name() + "_grp" ))
    oneGroup.setParent(sel)
    oneGroup.translate.set([0,0,0])
    oneGroup.rotate.set([0,0,0])
    
    pm.parent(oneGroup, w = True)
    sel.setParent(oneGroup)
    oneGroup.setParent(oldParent)
    return oneGroup


# get joints by grp name
jntGrp = pm.ls('facial_jnt_grp_bak')

bakJntList = []
for g in jntGrp:
    sel = pm.listRelatives(g, children = True, type = 'joint' )
    for s in sel:
        bakJntList.append(s)
    print(bakJntList)

# create copy of the group
sel = []
facJntGrp = createFacialGrp('facial_jnt_grp')
for jnt in bakJntList:
    newJoint = pm.duplicate(jnt, name = jnt.name().replace('_bak', ''))
    for n in newJoint:
        n.setParent(facJntGrp)
        sel.append(n)

# add freeze grp on new joints
for elt in sel:
    createZeroParent(elt)

#sel = pm.ls(sl = True)
facCtrlGrp = createFacialGrp('facial_ctrl_grp')
# mirrorGrp = createFacialGrp('facial_mirror_jnt_grp')

# mirror joints
mirrorList = []
for s in sel:
    if s.name().startswith('R_') and pm.nodeType(s) == 'joint':
        copyList = pm.duplicate(s, name = s.name().replace('R_', 'L_'))
        for elt in copyList:
            mirrorList.append(elt)
            newGroup = createZeroParent(elt)
            tempGrp = pm.group(em = True, world  = True, name = "tempMirrorGrp" )
            newGroup.setParent(tempGrp)
            # reverse
            tempGrp.scaleX.set(-1)
            # unparent group
            # reparent to facial
            newGroup.setParent(world = True)
            newGroup.setParent(facJntGrp)
            pm.delete(tempGrp)

# create controler
allJoints = sel + mirrorList
for s in allJoints:
    if (pm.nodeType(s) == 'joint'):
        s.setAttr('segmentScaleCompensate', False)
        grpTmp, circTmp = createCircle(s,[0,0,1])
        pm.parent(grpTmp, facCtrlGrp)
        pm.move('%s.cv[0:7]' % circTmp, [0, 0, 0.05],relative = True, objectSpace = True, worldSpaceDistance  = True )
        pm.parentConstraint(circTmp, s, maintainOffset = False, weight = 1 )