'''
Created on 4 mai 2015

@author: nicolas_2
'''
"""
copy foot x 2

find fkchain and ik chain
find switch ctrl

attach fk foot to fkchain
attach ikchain(followik) to reverse foot 

create reverse foot joint
attach foot deform system to reverse foot
attach foot deform system to fk chain

connect foot deform system attachement to ik ctrl

create foot on fkChain 
create ik chain on reverse foot
creat ikChain to reverse foot ctrl

create fkchain on toes 
attach toe system on foot deform

place ik ctrl on floor

"""
from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD
import maya.mel as mm
import maya.OpenMaya as om

sel = pm.ls(sl = True)

"""
# looking for ik and fk chain
for s in sel:
    links = pm.listConnections(s, type = "parentConstraint")
#     for l in links: print pm.nodeType(l)
    for l in links: 
#         print pm.nodeType(l)
        if pm.nodeType(l) == "parentConstraint":
            test = pm.parentConstraint(l, query = True, targetList = True)
#             print (test)
            test2 = pm.parentConstraint(l, query = True, weightAliasList  = True)
#             print (test2)
            test3 = pm.listConnections(l, connections = False, source  = True, exactType = True,  destination = False, type = "transform")
            print (test3)
            break
"""
Rankle = None
Rend = None
Rtoes = None
Rball = None
Rheel = None

# find foot joint order
for s in sel:
  
    allJnt = pm.listRelatives(s, allDescendents = True, type= "joint")
    for j in allJnt:
        if (j.getAttr("side") == 2):
            if(j.getAttr("type") == 18):
                print(j.getAttr("otherType"))
                if (j.getAttr("otherType") == "ankle"):
                    Rankle = j
                elif (j.getAttr("otherType") == "end"):
                    Rend = j
                elif (j.getAttr("otherType") == "toes"):
                    Rtoes = j
                elif (j.getAttr("otherType") == "ball"):
                    Rball = j
                elif (j.getAttr("otherType") == "heel"):
                    Rheel = j

footAr = [Rankle, Rend, Rtoes, Rball, Rheel ]             
print footAr


# sel = pm.ls(sl = True)[0]
# attrs = pm.listAttr(sel)
# pprint(attrs)
# print(pm.nodeType(sel))