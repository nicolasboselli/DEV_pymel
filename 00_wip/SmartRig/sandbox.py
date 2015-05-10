import cleanPipeline.cleanModules as clean
from multiprocessing import Condition
from math import ceil
reload(clean)
clean.cleanModules()

from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD



sel = pm.ls(sl = True)[0]

defSys = SRD.initDeformSystem()
motSys = SRD.initMotionSystem()


def createOneAlias(sel = None):
    rootGrp, rootHlp = helpers.createOneHelper( sel = sel, freezeGrp = True, hierarchyParent = "motion_system", constraintFrom = sel, suf= "_alias")
    childJoints = pm.listRelatives(sel, children = True, type = "joint")
    if len(childJoints)>0:
        for j in childJoints:
            helpers.createOneHelper( sel = j, type = "loc", freezeGrp = True, hierarchyParent = rootHlp, suf = "_alias")
            
        

    
createOneAlias(sel = sel)