'''
Created on 28 avr. 2015

@author: nico
'''
from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.AddAttr as ikAttr
import SmartRig.IKFK.SmartRigDef as SRD

motSys = None
for x in pm.ls("motion_system"):
    if pm.nodeType(x) == "transform":
        motSys = x
        break

print motSys
if motSys:
    allCtrlShape = pm.listRelatives(motSys, allDescendents = True, type = "nurbsCurve")
    ctrlSet = pm.sets(name = "controls")
    for o in allCtrlShape:
        ctrl = o.listRelatives(parent = True)
        pm.sets(ctrlSet, edit = True, addElement = ctrl )
        
        
# test = pm.PyNode("R_ring_03_ctrlShape")
# 
# pprint(pm.listRelatives(test, parent=True))