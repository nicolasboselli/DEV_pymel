'''
Created on 23 nov. 2014

@author: nicolas_2
'''

### recommandation: le script est pense pour des joints qui pointe vers le joint suivant, qui rotate sur y 

# selection

import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
reload(clean)
clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import IKFK.AddAttr as ikAttr

sel = pm.ls(sl = True)

# TODO: reorganize motion system with ik and fk
# TODO: add controller on pole Vector
# TODO: change controllers Color
# TODO: change controllers scale
# TODO: add resize
# TODO: hide ik and fk joint

########################################################################## BASE CREATION
# get joint radius
rad = sel[0].radius.get()

# duplicate selection FK 
fkChain = pm.duplicate(sel, renameChildren = True)
for jnt in fkChain:
    pm.rename(jnt, jnt.name() + "_FK")
    jnt.radius.set(rad*1.2)
# fkChain[0].setAttr('translateX', -2)

# duplicate selection IK
ikChain = pm.duplicate(sel, renameChildren = True)
for jnt in ikChain:
    pm.rename(jnt, jnt.name() + "_IK")
    jnt.radius.set(rad*1.4)
# ikChain[0].setAttr('translateX', 2)


jtRoot = helpers.rootGroup([sel[0]])[0]
fkRoot = helpers.rootGroup([fkChain[0]])[0]
ikRoot = helpers.rootGroup(sel = [ikChain[0]])[0]


tmpGrp = pm.group(em = True)
pm.rename(tmpGrp, '%s_IKFK_grp' % sel[0])

motionGrp = pm.group(em = True, name = 'motion_system')
defGrp = pm.group(em = True, name = 'deformation_system')

motionGrp.setParent(tmpGrp)
defGrp.setParent(tmpGrp)

jtRoot.setParent(defGrp)
ikRoot.setParent(motionGrp)
fkRoot.setParent(motionGrp)

motionGrp.setParent(tmpGrp)
defGrp.setParent(tmpGrp)


#############################################################################################switch IKFK

# TODO: ajouter scale constraint on deform joints
# create ctrl with switch ikfk
switchIKFK = pm.circle(ch = False, o = True, nr = [0,1,0], r = 1, name = 'switchIKFK' )
pm.addAttr(switchIKFK, ln =  "fk" , at  = 'double', min = 0, max = 1)
pm.addAttr(switchIKFK, ln =  "ik" , at  = 'double', min = 0, max = 1)
pm.addAttr(switchIKFK, ln =  "fkVis" , at  = 'bool')
pm.addAttr(switchIKFK, ln =  "ikVis" , at  = 'bool')
pm.addAttr(switchIKFK, ln =  "autoVis" , at  = 'bool')
pm.setAttr('switchIKFK.fk', keyable = True)
pm.setAttr('switchIKFK.ik', keyable = True)
pm.setAttr('switchIKFK.fkVis', channelBox = True)
pm.setAttr('switchIKFK.ikVis', channelBox = True)
pm.setAttr('switchIKFK.autoVis', channelBox = True)

constNode = pm.shadingNode('addDoubleLinear', asUtility = True )
constNode.setAttr('input1', 1)
subNode = pm.shadingNode('plusMinusAverage', asUtility = True )
subNode.setAttr('operation', 2)
pm.connectAttr('%s.output' % constNode.name(), '%s.input1D[0]' % subNode.name(), f = True)
pm.connectAttr('%s.fk' % switchIKFK[0].name(), '%s.input1D[1]' % subNode.name(), f = True)
pm.connectAttr('%s.output1D' % subNode.name(), '%s.ik' % switchIKFK[0].name(), f = True)

# add parent constraints on sel
for i, jnt in enumerate(sel):
    constrain = pm.parentConstraint(fkChain[i], ikChain[i], sel[i])
    constrainList = pm.listAttr(constrain, visible = True, keyable= True)
    for attr in pm.listAttr(constrain, visible = True, keyable= True):
        if 'IK' in attr:
            print(attr)
            pm.connectAttr('%s.ik' % switchIKFK[0].name(), '%s.%s' % (constrain,attr))
        elif 'FK' in attr:
            print(attr)
            pm.connectAttr('%s.fk' % switchIKFK[0].name(), '%s.%s' % (constrain,attr))

switchGrp = helpers.rootGroup(switchIKFK)[0]
switchGrp.setParent(motionGrp)

#     pm.connectAttr('%s.fk' % switchIKFK[0].name(), constrain)

################################################################################ create FK
# add crtl
# constrain joints to ctrls
for j in fkChain:
    print j
fkCtrls = helpers.createCircle([1,0,0], fkChain)


for i in range(len(fkCtrls)-1, 0, -1):
    tmpChild = fkCtrls[i].getParent()
    tmpChild.setParent(fkCtrls[i-1])
    
for i, null in enumerate(fkCtrls):
    pm.parentConstraint(fkCtrls[i], fkChain[i])
    pm.scaleConstraint(fkCtrls[i], fkChain[i])
    
tmpChild = fkCtrls[0].getParent()
tmpChild.setParent(motionGrp)


# IK
############################################################################# create ik
ikTmp = pm.ikHandle(startJoint = ikChain[0], endEffector = ikChain[-1])
ikHandle = ikTmp[0]


# create pole vector locator
poleVectorLoc = pm.spaceLocator()
pm.rename(poleVectorLoc, 'poleVectorLoc')

constraint = pm.parentConstraint(ikChain[1], poleVectorLoc)
pm.delete(constraint)

pm.parent(poleVectorLoc.name(), ikChain[1].name())
poleVectorLoc.setAttr("translateZ", 1)
pm.parent(poleVectorLoc.name(), world = True)

# change iksolver to rotate plane solver
ikSolver = pm.createNode("ikRPsolver")
pm.disconnectAttr("%s.ikSolver" % ikHandle.name())
pm.connectAttr("%s.message" % ikSolver.name(), "%s.ikSolver" % ikHandle.name())

# create pole vector
pm.poleVectorConstraint(poleVectorLoc, ikHandle, weight = 1)

#rotate du locator a zero
poleVectorLoc.rotate.set([0,0,0])

# add ik control
ikCtrl = helpers.createCircle([1,0,0], [ikHandle])[0]
pm.pointConstraint(ikCtrl, ikHandle)

ikHandle.setParent(motionGrp)
(ikCtrl.getParent()).setParent(motionGrp)
poleVectorLoc.setParent(motionGrp)

############################################################################################### pole vector multiple parent


############################################################################################     add stretch sur ik
ikAttr.addAttrIK(sel = [ikCtrl])

#         distance hankle knee
distSel = [ikRoot, ikCtrl]
distShape, locs = helpers.creatDist(sel = distSel)

tmpChild = distShape.getParent()

distGrp = pm.group(em = True)
distGrp.rename('%s_grp' % distShape.name())
tmpChild.setParent(distGrp)
for l in locs:
    l.setParent(distGrp)

distGrp.setParent(motionGrp)
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

#         multiplydivide
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

pprint(pm.listAttr(stretchCond))

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

pm.connectAttr(finalStretch_sum.output1D, ikChain[0].sx )
pm.connectAttr(finalStretch_sum.output1D, ikChain[1].sx )

# add lock on pole vector
# add resize on ik
# add squash and stretch

# 
# 