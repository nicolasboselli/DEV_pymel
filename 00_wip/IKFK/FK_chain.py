'''
Created on 23 avr. 2015

@author: nicolas_2
'''
import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
reload(clean)
clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import IKFK.SmartRigDef as SRD

# init hierarchy
# create hierarchy
motionGrp = SRD.initMotionSystem ()
defGrp = SRD.initDeformSystem ()


sel = pm.ls(sl = True)

# find and collect all children in hierarchy
jointList = []
jointList.append(sel[0])
children = pm.listRelatives(sel[0], allDescendents = True, type = 'joint')
for i in range((len(children)-1),0,-1):
    if  len(children[i].getChildren()) > 0:
        jointList.append(children[i])

# create controller
fkCtrls = helpers.createCircle([1,0,0], sel = jointList, radius = 1)


# parent controller, create fk chain
for i in range(len(fkCtrls)-1, 0, -1):
    tmpChild = fkCtrls[i].getParent()
    tmpChild.setParent(fkCtrls[i-1])

for i, null in enumerate(fkCtrls):
    pm.parentConstraint(fkCtrls[i], jointList[i])
    pm.scaleConstraint(fkCtrls[i], jointList[i])

# parent fk_chain to motion_system
tmpChild = fkCtrls[0].getParent()
tmpChild.setParent(motionGrp)
