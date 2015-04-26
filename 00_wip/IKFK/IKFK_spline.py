'''
Created on 24 avr. 2015

@author: nicolas_2
'''
import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
reload(clean)
clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import ctrlShape.ctrlShapes as ctrlShapes
import IKFK.AddAttr as ikAttr
import IKFK.SmartRigDef as SRD

"""
on selection
    Xduplicate joint chain
    
    Xsubdivide joint chain (joint number x 3)
    
    Xcreate ikhandle
    Xcreate spline
    
    Xon each cv of the curve create one cluster
    on each cluster create one controller
    parent little controller to bigger controller
    constrain deformation to motion system
    twist spine
    stretch on joint chain
"""

sel = pm.ls(sl = True)
# try:
#     pm.delete("motion_system")
# except:
#     pass

# create hierarchy
motionGrp = SRD.initMotionSystem ()
defGrp = SRD.initDeformSystem ()

def collectAllChild (sel):
    jointList = []
    jointList.append(sel[0])
    children = pm.listRelatives(sel[0], allDescendents = True, type = 'joint')
    for i in range((len(children)-1),0,-1):
        if  len(children[i].getChildren()) > 0:
            jointList.append(children[i])
    return jointList


# CompleteHierarchy = collectAllChild (sel)
# workingCopy = pm.duplicate(CompleteHierarchy, parentOnly = True, renameChildren = True)

#create working copy
workingCopy = pm.duplicate(sel, parentOnly = True, renameChildren = True)
rootGrp = helpers.rootGroup([workingCopy[0]])[0]
rootGrp.rename("IKFK_spine_%s" % rootGrp.nodeName())
rootGrp.setParent(motionGrp)

# insert joints
for jnt in workingCopy:
    child = jnt.getChildren()
    if len(child)>0:
        num = 3
        rad = pm.joint(jnt, query = True , radius = True)[0]
        dist = pm.joint(child[0], query = True , relative = True, position = True)[0]
        gap = dist/(num)
        for i in range((num-1),0,-1):
            newJnt = pm.insertJoint(jnt)
            pm.joint( newJnt, edit = True,component = True, relative = True, radius = rad, position = ((gap*i),0,0))

# create ikhandle
IKspine = pm.ikHandle(solver = "ikSplineSolver" ,name = "IKspine",startJoint = workingCopy[0], endEffector = workingCopy[(len(workingCopy)-1)], createCurve = True, numSpans = 4)
IKcurve = IKspine[2]

IKspine[0].setParent(rootGrp)
curveJointList = pm.ikHandle(IKspine[0], query = True, jointList = True)

# create clusters on point
cvsList = (IKcurve.getShape()).getCVs()

clusterGrp = pm.group(name = "cluster_grp", empty = True)
pprint(clusterGrp)
clusterGrp.setParent(rootGrp)

ctrlGrp = pm.group(name = "ctrls_grp", empty = True)
pprint(ctrlGrp)
ctrlGrp.setParent(rootGrp)

ctrlList = []
clusterList = []
for i,cv in enumerate(cvsList):
    tmpCluster = pm.cluster("curve1.cv[%s]" % i)[1]
    tmpCluster.setParent(clusterGrp)
    clusterList.append(tmpCluster)
    
    oneCtrl = ctrlShapes.createNurbsSphere()
    ctrlList.append(oneCtrl)
#     oneCtrl.setParent(ctrlGrp)

for c in ctrlList:
    c.setParent(ctrlGrp)
#     tmpClusctrlListter.setParent(oneCtrl)


