
import os, sys

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

def hideJoints():
#     error non joint type
    joints = pm.ls(type = 'joint')
    for j in joints:
        pm.setAttr('%s.drawStyle' % j, 2)
    
def showJoints():
#     error non joint type
    joints = pm.ls(type = 'joint')
    for j in joints:
        pm.setAttr('%s.drawStyle' % j, 0)

def resizeJoints(jointSize = 5, all = True):
#     error non joint type
    joints = []
    if all:
        joints = pm.ls(type = 'joint')
    else:
        sel = pm.ls(sl=True)
        for s in sel:
            if pm.nodeType(s) == 'joint':
                joints.append(s)
        
    
    for j in joints:
        pm.setAttr('%s.radius' % j, jointSize)

def displayJointOrient(state = True):
#     error non joint type
    sel = pm.ls(sl = True)
    for s in sel:
        pm.setAttr('%s.jointOrientX' % s.name(), k = state)
        pm.setAttr('%s.jointOrientY' % s.name(), k = state)
        pm.setAttr('%s.jointOrientZ' % s.name(), k = state)
    print('done display')

def freezeJoint():
#     error non joint type
    sel = pm.ls(sl = True)
    for s in sel:
        pm.makeIdentity(s,  apply = True, t =0,  r =1,  s= 0, n= 0, pn= 1)

def displayLocalAxis(state = 0):
    sel = pm.ls(sl = True)
    for s in sel:
        pm.setAttr('%s.displayLocalAxis' % s.name(), state)        
        


