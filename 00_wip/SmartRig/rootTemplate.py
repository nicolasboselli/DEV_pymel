'''
Created on 1 juin 2015

@author: nico
'''



import sys


import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.FK_chain as FK
import SmartRig.ManageCtrls.manageCtrls_def as MC
import SmartRig.IKFK.SmartRigDef as SRD
reload(helpers)

"""
maj:6
    parent ik handle and pole vector to root ctrl
"""


# create hierarchy
def createRigRoot(sel):
    motionGrp = SRD.initMotionSystem ()
    defGrp = SRD.initDeformSystem ()
    
    for s in sel:
        if checkSel(s):
            bodyCtrlGrp, bodyCtrl = helpers.createOneHelper(sel = s, axis = [1,0,0], type = "circle", scale=6, freezeGrp = True)
            pm.rename(bodyCtrl, "body_ctrl")
            pm.rename(bodyCtrlGrp, "body_ctrl_grp")
            pm.parentConstraint(bodyCtrl, s)
            
            rootCtrlGrp, rootCtrl = helpers.createOneHelper(type = "cross", scale=15, freezeGrp = True)
            pm.rename(rootCtrl, "root_ctrl")
            pm.rename(rootCtrlGrp, "root_ctrl_grp")
            pm.parent(bodyCtrlGrp, rootCtrl)
        
            pm.parent(rootCtrlGrp, motionGrp)
            
def checkSel(sel):
    return True
    
    
sel = pm.ls(sl = True)
createRigRoot(sel = sel)