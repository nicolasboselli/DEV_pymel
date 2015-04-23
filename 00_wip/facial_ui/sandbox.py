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


def createZeroParent():
    sel = pm.ls(sl = True)[0]
    oldParent = pm.listRelatives(sel, allParents = True)
    oneGroup = pm.group(em = True, name = ( sel.name() + "_grp" ))
    oneGroup.setParent(sel)
    oneGroup.translate.set([0,0,0])
    oneGroup.rotate.set([0,0,0])
    
    pm.parent(oneGroup, w = True)
    sel.setParent(oneGroup)
    oneGroup.setParent(oldParent)
    return oneGroup


#### symmetrize control
# select a control and the def will symetrize the controller with his group withoout the children and rename
def symCtrl(s, root):
    parent = pm.listRelatives(s, parent = True)
    children = pm.listRelatives(s, children = True, type = 'transform')
    # deparent children
    for c in children:
        c.setParent(world = True)
    # duplicate group parent
    for p in parent :
        newGroup = pm.duplicate(parent, renameChildren = True, name = p.name().replace('R_', 'L_'))
    # rename children
    child = pm.listRelatives(newGroup, children = True, type = 'transform')
    
    print(child)
    for c in child:
        pm.rename(c, c.name().replace('R_', 'L_'))
    # reparent children
    for c in children:
        c.setParent(s)
        # deparent copy 
        print(children)
    
    tempGrp = pm.group(em = True, world  = True, name = "tempMirrorGrp" )
    for grp in newGroup:
        grp.setParent(tempGrp)
     # reverse
        tempGrp.scaleX.set(-1)
    # parent copy group parent to world to world
        grp.setParent(world = True)
    # parent copy to facial 'facial_ctrl_grp'
        grp.setParent(root)
        pm.delete(tempGrp)

# rescale circle shape
def rescaleShape(s):
    pm.scale('%s.cv[0:7]' % s, [0.5, 0.5, 1],relative = True, objectSpace = True)

def createCircle(sel, axis):
#     sel = pm.ls(sl = True)[0]
    print sel
    oneCircle = pm.circle(n = (sel.name().replace('_jnt', '') + "_ctrl"), ch = True, o = True, nr = axis, r =0.1)[0]
    print oneCircle
    oneGroup = pm.group(em = True, name = ( oneCircle.name().replace('_ctrl', '_grp')))
    
    oneCircle.setParent(oneGroup)
    pm.parent(oneGroup, sel, r = True)
    pm.parent(oneGroup, w = True)
    return oneGroup, oneCircle

facJntGrp = 'facial_ctrl_grp'

sel = pm.ls(sl = True)
for s in sel:
    symCtrl(s, facJntGrp)

sel = pm.ls(sl = True)
for s in sel:
    rescaleShape(s)

sel = pm.ls(sl = True)
for s in sel:
    createCircle(s, [1,0,0])




