'''
Created on 23 avr. 2015

@author: nicolas_2
'''

"""
respect hierarchy
"""

# import cleanPipeline.cleanModules as clean
# from multiprocessing import Condition
# reload(clean)
# clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD
import maya.mel as mm
import maya.OpenMaya as om


# sel = pm.ls(sl = True)
def collectAllChild (sel):
    jointList = []
    jointList.append(sel)
    children = pm.listRelatives(sel, allDescendents = True, type = 'joint')
    for i in range((len(children)-1),0,-1):
        if  len(children[i].getChildren()) > 0:
            jointList.append(children[i])
    return jointList


def createOneFKChain(jointList = None, radius = 1, theSuffix = "_FK_ctrl", axis = [1,0,0] ):
    # create controller
    fkCtrlsGrp, fkCtrls = helpers.createCircle(axis=axis, sel = jointList, radius = radius, suffix = theSuffix)
    
    # create controller hierachy 
    for i in range(len(fkCtrls)-1, 0, -1): fkCtrlsGrp[i].setParent(fkCtrls[i-1])

    # constraint joint to controllers
    for i, null in enumerate(fkCtrls):
        pm.parentConstraint(fkCtrls[i], jointList[i])
        pm.scaleConstraint(fkCtrls[i], jointList[i])
    
    return fkCtrlsGrp, fkCtrls
   

def createFKchain (sel = None, collectHierarchy = True, rad = 1, theSuffix = "_FK_ctrl", axis = [1,0,0], linkChain = False, returnCtrls = False, hideSystem = True):
    
    motionGrp = SRD.initMotionSystem ()
    defGrp = SRD.initDeformSystem ()
    
    # find and collect all children in hierarchy
    if not sel:
        om.MGlobal_displayError("selection none")
        return
    
    fkCtrls = []
    tmpChild = []
    if collectHierarchy:
        for s in sel:
            jointList = collectAllChild(s)
                    # create controller
            fkCtrlsGrp, fkCtrls = createOneFKChain(jointList = jointList, theSuffix = theSuffix, radius = rad, axis= axis )
            
            # parent fk_chain to motion_system
            fkCtrlsGrp[0].setParent(motionGrp)
            tmpChild.append(fkCtrlsGrp[0])
            
    else:
        fkCtrlsGrp, fkCtrls = createOneFKChain(jointList = sel, theSuffix = theSuffix, radius = rad, axis= axis)
        
        # parent fk_chain to motion_system
        fkCtrlsGrp[0].setParent(motionGrp)
        tmpChild.append(fkCtrlsGrp[0])
        
    if  linkChain:
        chainAnchor = sel[0].getParent()
        pm.parentConstraint(chainAnchor, tmpChild, maintainOffset = True)
    
    if hideSystem:
        sel[0].visibility.set(0)
    
    if not returnCtrls:
        return tmpChild
    else:
        return tmpChild, fkCtrls
    

# createFKchain(sel = pm.ls(sl = True), linkChain = True)