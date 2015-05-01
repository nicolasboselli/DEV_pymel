'''
Created on 23 nov. 2014

@author: nicolas_2
'''

# ## recommandation: le script est pense pour des joints qui pointe vers le joint suivant en x, qui rotate sur y 

# selection

"""
maj:
    - reorganize motion_system with ik and fk
    
    x- constraint joint hand wriste to ik
    - add resize on ik
    - add squash on ik
    - connect ctrls vis
    - hide ikfk motion_system
    x- make pole vector ctrl a cube
    x- make switch ctrl a cross
    x- change controllers size
    - change controllers Color
"""

import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
reload(clean)
clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.AddAttr as ikAttr
import SmartRig.IKFK.SmartRigDef as SRD
import SmartRig.IKFK.FK_chain as FKdef

import maya.mel as mm
import maya.OpenMaya as om




########################################################################## BASE CREATION
# get joint radius
sel = pm.ls(sl=True)
rad = sel[0].radius.get()

# create hierarchy
motionGrp = SRD.initMotionSystem ()
defGrp = SRD.initDeformSystem ()

def createIKFK (sel):
    pass

# duplicate selection FK 
fkChain = pm.duplicate(sel, renameChildren=True, parentOnly=True)
for jnt in fkChain:
    pm.rename(jnt, jnt.name() + "_FK")
    jnt.radius.set(rad * 1.2)

# duplicate selection IK
ikChain = pm.duplicate(sel, renameChildren=True, parentOnly=True)
for jnt in ikChain:
    pm.rename(jnt, jnt.name() + "_IK")
    jnt.radius.set(rad * 1.4)

# jtRoot = helpers.rootGroup([sel[0]])[0]
fkRoot = helpers.rootGroup([fkChain[0]])[0]
ikRoot = helpers.rootGroup(sel=[ikChain[0]])[0]

# IKFK grp creation
tmpGrp = pm.group(em=True)
pm.rename(tmpGrp, '%s_IKFK_grp' % sel[0])
tmpGrp.setParent(motionGrp)

ikRoot.setParent(tmpGrp)
fkRoot.setParent(tmpGrp)


################################################################################ create FK
# add FK crtl

fkroot = FKdef.createFKchain(sel = fkChain, collectHierarchy = False, rad = 2.5)
fkroot[0].setParent(fkRoot)

# IK
############################################################################# create ik
ikTmp = pm.ikHandle(startJoint=ikChain[0], endEffector=ikChain[-1])
ikHandle = ikTmp[0]

# create pole vector locator
poleVectorLoc = pm.spaceLocator()
pm.rename(poleVectorLoc, 'poleVectorLoc')

pm.parent(poleVectorLoc, ikChain[1])
poleVectorLoc.translate.set(0,0, -1)
pm.parent(poleVectorLoc.name(), world=True)


# change iksolver to rotate plane solver
ikSolver = pm.createNode("ikRPsolver")
pm.disconnectAttr("%s.ikSolver" % ikHandle.name())
pm.connectAttr("%s.message" % ikSolver.name(), "%s.ikSolver" % ikHandle.name())

# constrain pole vector
pm.poleVectorConstraint(poleVectorLoc, ikHandle, weight=1)
PVctrlGrp, PVctrl = helpers.createOneHelper(type = "cube", sel = poleVectorLoc, scale = 0.5)
poleVectorLoc.setParent(PVctrl)
PVctrlGrp.setParent(tmpGrp) 

# rotate du locator a zero
poleVectorLoc.rotate.set([0, 0, 0])

# add ikhandle controller
ikCtrlGrp, ikCtrl = helpers.createOneCircle(axis = [1, 0, 0], sel=sel[len(sel)-1])
pm.pointConstraint(ikCtrl, ikHandle)
ikHandle.setParent(tmpGrp)
ikCtrlGrp.setParent(tmpGrp)

pm.addAttr(ikCtrl, ln="_______" , attributeType="enum", enumName="CTRLS:")
pm.addAttr(ikCtrl, ln="autoStretch" , at='double', min=0, max=1, dv = 0)
pm.addAttr(ikCtrl, ln="followCtrl" , at='double', min=0, max=1, dv = 1)
pm.addAttr(ikCtrl, ln="followJoint" , at='double', min=0, max=1, dv = 0)
pm.addAttr(ikCtrl, ln="lockElbow" , at='double', min=0, max=1, dv = 0)
pm.addAttr(ikCtrl, ln="squash" , at='double', min=0, max=1, dv = 0)

pm.setAttr(ikCtrl._______ , keyable=True, lock=True)
pm.setAttr(ikCtrl.autoStretch , keyable=True)
pm.setAttr(ikCtrl.followCtrl , keyable=True)
pm.setAttr(ikCtrl.followJoint , keyable=True)
pm.setAttr(ikCtrl.lockElbow , keyable=True)
pm.setAttr(ikCtrl.squash , keyable=True)

subFollowNode = pm.createNode('plusMinusAverage')
subFollowNode.setAttr("input1D[0]", 1)
subFollowNode.setAttr('operation', 2)
pm.connectAttr(ikCtrl.followCtrl, subFollowNode.input1D[1], f = True)
pm.connectAttr(subFollowNode.output1D, ikCtrl.followJoint, f = True)

# create follow orient joint
ikOrientLoc = helpers.createOneLoc(ikChain[2])
ikOrientLoc.setParent(tmpGrp)
constrain = pm.orientConstraint(ikCtrl, ikChain[2], ikOrientLoc)
pm.pointConstraint(ikChain[2], ikOrientLoc)

followJoint = pm.duplicate(ikChain[2], name = ("%s_follow" % ikChain[2].nodeName()))[0]
followJoint.setParent(ikOrientLoc)
followJoint.rotate.set(0,0,0)
followJoint.translate.set(0,0,0)

for attr in pm.listAttr(constrain, visible = True, keyable= True):
            if 'IK' in attr:
                print(attr)
                pm.connectAttr(ikCtrl.followJoint, '%s.%s' % (constrain,attr))
            elif 'ctrl' in attr:
                print(attr)
                pm.connectAttr(ikCtrl.followCtrl, '%s.%s' % (constrain,attr))

############################################################################################### pole vector multiple parent


############################################################################################     add stretch sur ik

#         distance hankle knee
distSel = [ikRoot, ikCtrl]
distShape, locs = helpers.creatDist(sel=distSel)

tmpChild = distShape.getParent()

distGrp = pm.group(em=True)
distGrp.rename('%s_grp' % distShape.nodeName())
tmpChild.setParent(distGrp)
for l in locs: l.setParent(distGrp)

distGrp.setParent(tmpGrp)
#     calculate maximum leg size
#         plusMinusAverage
fixedSize_sumNode = pm.createNode('plusMinusAverage')
pm.rename(fixedSize_sumNode, 'fixedSize_sum')

pm.connectAttr(ikChain[1].tx, fixedSize_sumNode.input1D[0])
pm.connectAttr(ikChain[2].tx, fixedSize_sumNode.input1D[1])

#     create distance
pm.select(distShape)
        
#     calculate ratio leg fixed/stretched
stretchRatio_div = pm.createNode('multiplyDivide')
pm.rename(stretchRatio_div, 'stretchRatio_div')

#     multiplydivide
#             connect sum to multiply
pm.connectAttr(fixedSize_sumNode.output1D, stretchRatio_div.input2X)
#             connect distance to divide input1x
pm.connectAttr(distShape.distance, stretchRatio_div.input1X)
pm.setAttr(stretchRatio_div.operation, 2)

#     stretch Condition
stretchCond = pm.createNode('condition')
pm.rename(stretchCond, 'stretch_condition')

#         condition
pm.connectAttr(stretchRatio_div.outputX, stretchCond.firstTerm)
pm.setAttr(stretchCond.secondTerm, 1)
pm.connectAttr(stretchCond.firstTerm, stretchCond.colorIfTrueR)
pm.setAttr(stretchCond.operation, 2)

#     calculate maj
#         plusminusAverage
stretchMaj_sub = pm.createNode('plusMinusAverage')
pm.rename(stretchMaj_sub, 'stretchMaj_sub')
pm.connectAttr(stretchCond.outColorR, stretchMaj_sub.input1D[0])
pm.setAttr(stretchMaj_sub.input1D[1], 1)
stretchMaj_sub.operation.set(2)

#     strtch control variator
#         multiply divide
stretchVariation_multi = pm.createNode('multiplyDivide')
pm.rename(stretchVariation_multi, 'stretch_Variation_multi')
pm.connectAttr(stretchMaj_sub.output1D, stretchVariation_multi.input1X)
pm.connectAttr(ikCtrl.autoStretch, stretchVariation_multi.input2X)

#     calculate final
#         plusminusaverage
finalStretch_sum = pm.createNode('plusMinusAverage')
pm.rename(finalStretch_sum, 'finalStretch_sum')
finalStretch_sum.input1D[0].set(1)
pm.connectAttr(stretchVariation_multi.outputX, finalStretch_sum.input1D[1])

pm.connectAttr(finalStretch_sum.output1D, ikChain[0].sx)
pm.connectAttr(finalStretch_sum.output1D, ikChain[1].sx)

####################################################################################### add resize on ik
####################################################################################### add squash on ik


####################################################################################### switch IKFK
# create ctrl with switch ikfk
switchIKFKgrp, switchIKFK = helpers.createOneHelper(type= "cross", sel = sel[0], scale = 0.5, suf = "_switchIKFK")

pm.addAttr(switchIKFK, ln="_______" , attributeType="enum", enumName="CTRLS:")
pm.addAttr(switchIKFK, ln="fk" , at='double', min=0, max=1)
pm.addAttr(switchIKFK, ln="ik" , at='double', min=0, max=1)
pm.addAttr(switchIKFK, ln="fkVis" , at='bool')
pm.addAttr(switchIKFK, ln="ikVis" , at='bool')
pm.addAttr(switchIKFK, ln="autoVis" , at='bool')

pm.setAttr(switchIKFK._______ , keyable=True, lock=True)
pm.setAttr(switchIKFK.fk, keyable=True)
pm.setAttr(switchIKFK.ik, keyable=True)
pm.setAttr(switchIKFK.fkVis, channelBox=True)
pm.setAttr(switchIKFK.ikVis, channelBox=True)
pm.setAttr(switchIKFK.autoVis, channelBox=True)


subNode = pm.createNode('plusMinusAverage')
subNode.setAttr("input1D[0]", 1)
subNode.setAttr('operation', 2)

pm.connectAttr(switchIKFK.fk, '%s.input1D[1]' % subNode.nodeName(), f=True)
pm.connectAttr(subNode.output1D, '%s.ik' % switchIKFK.nodeName(), f=True)

# add parent constraints on sel
for i in range(0, (len(sel)),1):
    constrain = None
    if not (i == (len(sel)-1)): constrain = pm.parentConstraint(fkChain[i], ikChain[i], sel[i])
    else: constrain = pm.parentConstraint(fkChain[i], followJoint, sel[i])
    
    for attr in pm.listAttr(constrain, visible=True, keyable=True):
        if 'IK' in attr:
            pm.connectAttr(switchIKFK.ik, '%s.%s' % (constrain, attr))
        elif 'FK' in attr:
            pm.connectAttr(switchIKFK.fk, '%s.%s' % (constrain, attr))

# place switch on skeleton
"""
add two group upper cross to orient it
"""
switchIKFKgrp.setParent(sel[0])
switchIKFKgrp.tz.set(3)
pm.pointConstraint(sel[0], switchIKFKgrp, maintainOffset  = True)
switchIKFKgrp.setParent(tmpGrp)

om.MGlobal_displayInfo("IKFK_done")
