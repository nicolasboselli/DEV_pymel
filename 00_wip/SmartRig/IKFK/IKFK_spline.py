'''
Created on 24 avr. 2015

@author: nicolas_2
'''
"""
maj: 
# add parametrable squash
hide motion_system
connect ctrlvis
edit circle_ctrls size
place switch_IKFK
rename correctly fk an ik controls
add follow on ik mid ctrl
add follow on fk chest
add follow on ik base ctrl

debug:
    twist on ik chain
"""



# import cleanPipeline.cleanModules as clean
# from multiprocessing import Condition
# from math import ceil
# reload(clean)
# clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.AddAttr as ikAttr
import SmartRig.IKFK.SmartRigDef as SRD
import SmartRig.ikCurve as SRikCurve
import SmartRig.IKFK.FK_chain as FKChain
import math


sel = pm.ls(sl = True)
rad = sel[0].radius.get()

# create hierarchy
motionGrp = SRD.initMotionSystem ()
defGrp = SRD.initDeformSystem ()

#create working copy
IK_chain = pm.duplicate(sel, parentOnly = True, renameChildren = True)
for jnt in IK_chain:
    pm.rename(jnt, jnt.name() + "_IK")
    jnt.radius.set(rad*1.4)

FK_chain = pm.duplicate(sel, parentOnly = True, renameChildren = True)
for jnt in FK_chain:
    pm.rename(jnt, jnt.name() + "_FK")
    jnt.radius.set(rad*1.4)

rootGrp = helpers.rootGroup([IK_chain[0]])[0]
rootGrp.rename("IKFK_spine_%s" % rootGrp.nodeName())
rootGrp.setParent(motionGrp)
FK_chain[0].setParent(rootGrp)

ikSpineGrp = helpers.insertGroups([IK_chain[0]])[0]
fkSpineGrp = helpers.insertGroups([FK_chain[0]])[0]


########################################### FK system

fkCtrlsRoot = FKChain.createFKchain(sel = FK_chain, collectHierarchy = False, theSuffix = "_FK_ctrl", rad = 4.5)
for fkRoot in fkCtrlsRoot:
    fkRoot.setParent(fkSpineGrp)

######################################### IK System
# insert joints
IKjointList = []
jointIt = 3
for jnt in IK_chain:
    IKjointList.append(jnt)
    child = jnt.getChildren()
    if len(child)>0:
        num = jointIt
        rad = pm.joint(jnt, query = True , radius = True)[0]
        dist = pm.joint(child[0], query = True , relative = True, position = True)[0]
        gap = dist/(num)
        for i in range((num-1),0,-1):
            newJnt = pm.insertJoint(jnt)
            pm.joint( newJnt, edit = True,component = True, relative = True, radius = rad, position = ((gap*i),0,0))
            IKjointList.append(newJnt)

print "check1"    
# create ikhandle
IKspine = pm.ikHandle(solver = "ikSplineSolver", name = "IKspine", simplifyCurve = True, startJoint = IK_chain[0], endEffector = IK_chain[(len(IK_chain)-1)], createCurve = True, numSpans = 4)
IKhandle = IKspine[0]
IKcurve = IKspine[2]

IKhandle.setParent(ikSpineGrp)
curveJointList = pm.ikHandle(IKhandle, query = True, jointList = True)

# create clusters on point
cvsList = (IKcurve.getShape()).getCVs()

clusterGrp = pm.group(name = "cluster_grp", empty = True)
clusterGrp.setParent(ikSpineGrp)

ctrlGrp = pm.group(name = "IK_ctrls_grp", empty = True)
ctrlGrp.setParent(ikSpineGrp)

# parent cluster to sphere
ctrlList = []
clusterList = []
for i,cv in enumerate(cvsList):
    cluster = pm.cluster("curve1.cv[%s]" % i)
    cluster[0].setAttr("relative", 1)
    tmpCluster = cluster[1]
    tmpCluster.setParent(clusterGrp)
    clusterList.append(tmpCluster)
    
    oneCtrl = helpers.createNurbsSphere(rad = 0.5)
    ctrlList.append(oneCtrl)
#     oneCtrl.setParent(ctrlGrp)
    tmpPoint = pm.pointConstraint(tmpCluster, oneCtrl)
    pm.delete(tmpPoint)
    pm.pointConstraint(oneCtrl, tmpCluster)
    
    
for c in ctrlList:
    c.setParent(ctrlGrp)

ctrlListGrp = helpers.insertGroups(ctrlList)

print "check253"
# create main ctrls
# orient up and down ctrls as joint selection
upCtrlGrp, upCtrl = helpers.createOneCircle([1,0,0], sel = sel[0], rad = 4, suf= "_IK_ctrl")
print "check2531"
dwCtrlGrp, dwCtrl = helpers.createOneCircle([1,0,0], sel = sel[len(sel)-1], rad = 4, suf= "_IK_ctrl")
idMid =  int((pm.datatypes.round(float(len(ctrlListGrp))/2)) - 1)
midCtrlGrp, midCtrl = helpers.createOneCircle([0,1,0], sel = ctrlList[idMid], rad = 4, suf= "_IK_ctrl")

print "check254"
upCtrlGrp.setParent(ctrlGrp)
dwCtrlGrp.setParent(ctrlGrp)
midCtrlGrp.setParent(ctrlGrp)
print "check255"

upLoc = helpers.createOneLoc(parentToWorld = False, s = upCtrl)
dwLoc = helpers.createOneLoc(parentToWorld = False, s = dwCtrl)
upLoc.setAttr("tz", 2)
dwLoc.setAttr("tz", 2)

# parent sphere ctrls to main ctrls
ctrlListGrp[0].setParent(upCtrl)
ctrlListGrp[1].setParent(upCtrl)
ctrlListGrp[idMid - 1].setParent(midCtrl)
ctrlListGrp[idMid].setParent(midCtrl)
ctrlListGrp[idMid + 1].setParent(midCtrl)
ctrlListGrp[(len(ctrlListGrp)-2)].setParent(dwCtrl)
ctrlListGrp[(len(ctrlListGrp)-1)].setParent(dwCtrl)

# add twist
# debug: replace object up rot by object
IKhandle.setAttr("dTwistControlEnable", 1)
IKhandle.setAttr("dWorldUpType", 2)
IKhandle.setAttr("dWorldUpAxis", 3)

pm.connectAttr(upLoc.worldMatrix, IKhandle.dWorldUpMatrix, force = True)
pm.connectAttr(dwLoc.worldMatrix, IKhandle.dWorldUpMatrixEnd, force = True)

# add parameters on upper control
try: pm.addAttr(dwCtrl, longName  = "________", attributeType  = "enum", enumName = "CTRLS:")
except: print(Exception)
try: pm.setAttr(dwCtrl.________, keyable = True, lock = True)
except: print(Exception)

# make stretch editable
try: pm.addAttr(dwCtrl, longName  = "stretch", attributeType  = "double", min = 0, max = 1, dv = 0) 
except: print(Exception)
try: pm.setAttr(dwCtrl.stretch, keyable = True)
except: print(Exception)
try: pm.addAttr(dwCtrl, longName  = "squash", attributeType  = "double", min = 0, max = 1, dv = 0)
except: print(Exception)
try: pm.setAttr(dwCtrl.squash, keyable = True)
except: print(Exception)
try: pm.addAttr(dwCtrl, longName  = "followJoint", attributeType  = "double", min = 0, max = 1, dv = 1)
except: print(Exception)
try: pm.setAttr(dwCtrl.followJoint, keyable = True)
except: print(Exception)
try: pm.addAttr(dwCtrl, longName  = "followCtrl", attributeType  = "double", min = 0, max = 1, dv = 0)
except: print(Exception)
try: pm.setAttr(dwCtrl.followCtrl, keyable = True)
except: print(Exception)

subFollowNode = pm.createNode('plusMinusAverage')
subFollowNode.setAttr("input1D[0]", 1)
subFollowNode.setAttr('operation', 2)
pm.connectAttr(dwCtrl.followJoint, subFollowNode.input1D[1], f = True)
pm.connectAttr(subFollowNode.output1D, dwCtrl.followCtrl, f = True)

# add stretch
newJointsNum = (len(IKjointList))

# add arclenght on curve
arcLenNode = pm.arclen(IKcurve, ch = True)
defaultSize = arcLenNode.getAttr("arcLength")

# multiply/divide default size by current size
mdNode = pm.createNode("multiplyDivide")
mdNode.setAttr("operation", 2 )
mdNode.setAttr("input2X", arcLenNode.getAttr("arcLength") )
pm.connectAttr(arcLenNode.arcLength, mdNode.input1X)

# average to calculate stretch addition : stretch - 1
addStretchNode = pm.createNode("plusMinusAverage", name = "add_stretch")
addStretchNode.setAttr("operation", 2)
pm.connectAttr(mdNode.outputX, addStretchNode.input1D[0])
addStretchNode.setAttr("input1D[1]", 1)

# multiplydivide to mutiply stretch addition by strecth parameter
stretchMultiplyNode = pm.createNode("multiplyDivide",  name = "multiply_stretch")
pm.connectAttr(addStretchNode.output1D, stretchMultiplyNode.input1X)
pm.connectAttr(dwCtrl.stretch, stretchMultiplyNode.input2X)

# average to addition 1 + stretch addition
addStretchFinalNode = pm.createNode("plusMinusAverage", name = "add_stretch")
addStretchFinalNode.setAttr("operation", 1)
pm.connectAttr(stretchMultiplyNode.outputX, addStretchFinalNode.input1D[0])
addStretchFinalNode.setAttr("input1D[1]", 1)

for jnt in IKjointList:
    jntNode =  (pm.PyNode(jnt))
    try:
        pm.connectAttr(addStretchFinalNode.output1D, jntNode.scaleX)
    except:
        print(Exception)
        
# add parametrable squash


# add follow on chest

lastJoint = IKjointList[len(IKjointList)-1]
IKfollowJnt = pm.duplicate(lastJoint, name = (lastJoint.nodeName() + "_follow"))[0]
IKfollowJnt.setAttr("scaleX", 1)
IKfollowJnt.setParent(ikSpineGrp)

"""
tmp = IKfollowJnt.getParent()
if tmp:
    tmp.setAttr("scaleX", 1)
    IKfollowJnt.setParent(world = True)
    pm.delete(tmp)
"""


constrain = pm.parentConstraint(dwCtrl, IK_chain[len(IK_chain)-1], IKfollowJnt)


for attr in pm.listAttr(constrain, visible = True, keyable= True):
            if 'IKW' in attr:
                print(attr)
                pm.connectAttr(dwCtrl.followJoint, '%s.%s' % (constrain,attr))
                ikFound = True
            elif 'ctrl' in attr:
                print(attr)
                pm.connectAttr(dwCtrl.followCtrl, '%s.%s' % (constrain,attr))


# constrain deformation system to motion system
    # create switch attribute
switchIKFK = pm.circle(ch = False, o = True, nr = [0,1,0], r = 1, name = 'switchIKFK_spine')[0]
switchIKFK.setParent(rootGrp)

pm.addAttr(switchIKFK, ln =  "_______" , attributeType  = "enum", enumName = "CTRLS:")
pm.addAttr(switchIKFK, ln =  "fk" , at  = 'double', min = 0, max = 1, dv = 1)
pm.addAttr(switchIKFK, ln =  "ik" , at  = 'double', min = 0, max = 1)
pm.addAttr(switchIKFK, ln =  "fkVis" , at  = 'bool')
pm.addAttr(switchIKFK, ln =  "ikVis" , at  = 'bool')
pm.addAttr(switchIKFK, ln =  "autoVis" , at  = 'bool')

pm.setAttr(switchIKFK._______ , keyable = True, lock = True)
pm.setAttr(switchIKFK.fk, keyable = True)
pm.setAttr(switchIKFK.ik, keyable = True)
pm.setAttr(switchIKFK.fkVis, channelBox = True)
pm.setAttr(switchIKFK.ikVis, channelBox = True)
pm.setAttr(switchIKFK.autoVis, channelBox = True)

subNode = pm.createNode('plusMinusAverage')
subNode.setAttr("input1D[0]", 1)
subNode.setAttr('operation', 2)

pm.connectAttr(switchIKFK.fk, subNode.input1D[1], f = True)
pm.connectAttr(subNode.output1D, switchIKFK.ik, f = True)

for i in range(0, (len(sel)),1):
    constrain = None
    if not (i == (len(sel)-1)): constrain = pm.parentConstraint(FK_chain[i], IK_chain[i], sel[i])
    else: constrain = pm.parentConstraint(FK_chain[i], IKfollowJnt, sel[i])

    if constrain:
        for attr in pm.listAttr(constrain, visible = True, keyable= True):
            if 'IK' in attr:
                print(attr)
                pm.connectAttr(switchIKFK.ik, '%s.%s' % (constrain,attr))
            elif 'FK' in attr:
                print(attr)
                pm.connectAttr(switchIKFK.fk, '%s.%s' % (constrain,attr))


