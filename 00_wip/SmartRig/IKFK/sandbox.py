'''
Created on 23 avr. 2015

@author: nicolas_2
'''


from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD
import maya.mel as mm
import maya.OpenMaya as om


def createFKChainHierarchy(sel):
    getChildren = True
    # while getChildren
    # for s in parent
    count = 0
    while len(sel)>0:
        for s in sel:
#             pprint(s)
            sel = pm.listRelatives(s, children = True, type = 'joint')
            pprint(sel)
#         count = count + 1
        # create controller on sel
        # find children
            # for each children create controller 
            # parent children controller on parent controller
                # find parent
                # find controller parent
        # if not children = false

# find all descendants

import SmartRig.IKFK.FK_chain as FK

sel = pm.ls(sl = True)[0]
jointList = FK.collectAllChild(sel)

for s in jointList:
    # find parent selection
    parentTmp = s.getParent()
    # find parent ctrl
    
    # create ctrl
    helpRoot, help = helpers.createOneHelper(type = "circle", sel = s, axis = [1,0,0], constraintTo = s)
    # if parent ctrl: parent root helper to parent ctrl
    if parentTmp:
        print"go parent"
        pprint(parentTmp)
        #find parent ctrl
        const = pm.listRelatives(parentTmp, type = "parentConstraint")[0]
        pprint(const)
        parentCtrl = pm.listConnections(const.target[0].targetTranslate)[0]
        pprint(parentCtrl)
        # attach new ctrlto parent
        helpRoot.setParent(parentCtrl)
        print"endParent parent"




# createFKChainHierarchy(sel = pm.ls(sl = True))