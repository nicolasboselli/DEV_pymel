'''
Created on 4 mai 2015

@author: nicolas_2
'''


from pprint import pprint
import pymel.core as pm
import SmartRig.createHelpers as helpers
import SmartRig.IKFK.SmartRigDef as SRD
import maya.mel as mm
import maya.OpenMaya as om
from pymel.core.general import PyNode
import SmartRig.IKFK.FK_chain as fkChain

reload(fkChain)

def findFeet(sel):
    R_foot = {}
    L_foot = {}
       
    # find foot joint order
    for s in sel:
        allJnt = pm.listRelatives(s, allDescendents = True, type= "joint")
        for j in allJnt:
            if (j.getAttr("side") == 2):
                if(j.getAttr("type") == 18):
                    print(j.getAttr("otherType"))
                    if (j.getAttr("otherType") == "ankle"):
                        R_foot["ankle"] = j
                    elif (j.getAttr("otherType") == "end"):
                        R_foot["end"] = j
                    elif (j.getAttr("otherType") == "toes"):
                        R_foot["toes"] = j
                    elif (j.getAttr("otherType") == "ball"):
                        R_foot["ball"] = j
                    elif (j.getAttr("otherType") == "heel"):
                        R_foot["heel"] = j
                        
            elif (j.getAttr("side") == 1):
                if(j.getAttr("type") == 18):
                    print(j.getAttr("otherType"))
                    if (j.getAttr("otherType") == "ankle"):
                        L_foot["ankle"] = j
                    elif (j.getAttr("otherType") == "end"):
                        L_foot["end"] = j
                    elif (j.getAttr("otherType") == "toes"):
                        L_foot["toes"] = j
                    elif (j.getAttr("otherType") == "ball"):
                        L_foot["ball"] = j
                    elif (j.getAttr("otherType") == "heel"):
                        L_foot["heel"] = j
    
    return R_foot,L_foot 

def initChain(dico):

    # looking for ik and fk chain
    switchCtrl = None
#     ikRoot = None
#     ikCtrl = None
#     jointTarget = []
#     endFKjoint = None
    
    if not dico["ankle"] or not dico["end"] or not dico["toes"] or not dico["ball"] or not dico["heel"]:
        return
    
    
#     links = pm.listConnections(dico["ankle"], type = "parentConstraint")
    
    
    parentConst = pm.listRelatives(dico["ankle"], type = "parentConstraint")[0]
    jointTarget = pm.parentConstraint(parentConst, query = True, targetList = True)
    
    # find ik end joint
    loc = jointTarget[1].getParent()
    pointConst = (pm.listRelatives(loc, type = "pointConstraint"))[0]
    endIKJoint = pm.pointConstraint(pointConst, query = True, targetList = True)[0]
    
    # find ik start joint
    ikEf = pm.listConnections(endIKJoint.translateX, type = "ikEffector")[0]
    ikHand =  pm.listConnections(ikEf.handlePath[0])[0]
    startIKJoint = pm.listConnections(ikHand.startJoint)[0]
    
    # find ik control
    constraint = pm.listConnections(ikHand.translateX)
    ikCtrl = pm.listConnections(constraint[0].target[0].targetParentMatrix)[0]
    
    # find jointTarget
    jointTarget = pm.parentConstraint(parentConst, query = True, targetList = True)
    
    # find fk end joint
    endFKjoint = jointTarget[0]
    
    # find switch ctrl
    switchCtrlTmp = pm.listConnections(parentConst, connections = False, source  = True, exactType = True,  destination = False, type = "transform")
    if len(switchCtrlTmp) > 1:
        for s in switchCtrlTmp:
            switchCtrl = s
            break
    
    return switchCtrl, startIKJoint, ikCtrl, jointTarget, endIKJoint, endFKjoint

def orientMirorredJoint(jnt, jntChild):
    jntChildPos = pm.duplicate(jntChild, name = (jntChild.nodeName() + "_positive_stretch_foot"), parentOnly = True)[0]
    bakPos = jntChild.translate.get()
#     print(bakPos)
    newPos = [bakPos[0]*-1,bakPos[1]*-1, bakPos[2]*-1 ]
#     print(newPos)
    jntChildPos.translate.set(newPos)
    jntChild.setParent(world = True)
    pm.joint(jnt, edit = True, orientJoint = "xzy", secondaryAxisOrient = "zup", zso = True )
    pm.delete(jntChildPos)
    jntChild.setParent(jnt)
    return om.MGlobal_displayInfo("orient done")

def createFKFoot(dico, parentGrp):
    fkGrp = pm.group(empty = True, name = "FK_joints")
    
    # create copy
    FK_foot_ankle = pm.duplicate(dico["ankle"], name = (dico["ankle"].nodeName() + "_FK_foot"), parentOnly = True)[0]
    FK_foot_end = pm.duplicate(dico["end"], name = (dico["end"].nodeName() + "_FK_foot"), parentOnly = True)[0]
    FK_foot_toes = pm.duplicate(dico["toes"], name = (dico["toes"].nodeName() + "_FK_foot"), parentOnly = True)[0]
    FK_foot_ball = pm.duplicate(dico["ball"], name = (dico["ball"].nodeName() + "_FK_foot"), parentOnly = True)[0]
    FK_foot_heel = pm.duplicate(dico["heel"], name = (dico["heel"].nodeName() + "_FK_foot"), parentOnly = True)[0]
    
    # create fk foot dico
    fkFootDico = {}
    fkFootDico["ankle"] = FK_foot_ankle
    fkFootDico["end"] = FK_foot_end
    fkFootDico["toes"] = FK_foot_toes
    fkFootDico["ball"] = FK_foot_ball
    fkFootDico["heel"] = FK_foot_heel
    
    # make hirarchy
    fkGrp.setParent(parentGrp)
    FK_foot_ankle.setParent(fkGrp) 
    FK_foot_ball.setParent(FK_foot_ankle)
    FK_foot_toes.setParent(FK_foot_ball)
    
    FK_foot_heel.setParent(FK_foot_ankle)
    FK_foot_end.setParent(FK_foot_heel)
    
    fkGrp, fkHlp = helpers.createOneHelper(sel = FK_foot_ankle,freezeGrp = True, hierarchyParent = "insert")
    
    # make fk foot system
    fkRoot = fkChain.createFKchain(sel = [FK_foot_ball, FK_foot_toes], collectHierarchy = False, rad = 5,  hideSystem = False )
    pprint(fkRoot)
    fkRoot[0].setParent(fkGrp)
    
    
    return [FK_foot_ankle, FK_foot_ball, FK_foot_toes, FK_foot_heel, FK_foot_end ], fkFootDico, fkGrp

def createReverseFoot(dico, parentGrp, stretchCtrl):
    """
    bug:
        -- transform on reverse foot
    """
    
    revGrp = pm.group(empty = True, name = "RevFoot_grp")
    
    # create grp from ctrl
    oneGrp, oneHlp = helpers.createOneHelper( sel = stretchCtrl , freezeGrp = True, hierarchyParent = "child")
    oneGrp.setParent(revGrp)
    
    # create copy
    Rev_foot_ankle_start = pm.duplicate(dico["ankle"], name = (dico["ankle"].nodeName() + "_start_Rev_foot"), parentOnly = True)[0]
    Rev_foot_heel = pm.duplicate(dico["heel"], name = (dico["heel"].nodeName() + "_Rev_foot"), parentOnly = True)[0]
    Rev_foot_end = pm.duplicate(dico["end"], name = (dico["end"].nodeName() + "_Rev_foot"), parentOnly = True)[0]
    Rev_foot_toes = pm.duplicate(dico["toes"], name = (dico["toes"].nodeName() + "_Rev_foot"), parentOnly = True)[0]
        # think to additive joint for toes
    Rev_foot_free_toes = pm.duplicate(dico["toes"], name = (dico["toes"].nodeName() + "_free_Rev_foot"), parentOnly = True)[0]
    Rev_foot_ball = pm.duplicate(dico["ball"], name = (dico["ball"].nodeName() + "_Rev_foot"), parentOnly = True)[0]
    Rev_foot_ankle_end = pm.duplicate(dico["ankle"], name = (dico["ankle"].nodeName() + "_end_Rev_foot"), parentOnly = True)[0]
    
    # create reverse foot dico
    revFootDico = {}
    revFootDico["ankle"] = Rev_foot_ankle_end
    revFootDico["end"] = Rev_foot_end
    revFootDico["toes"] = Rev_foot_free_toes
    revFootDico["ball"] = Rev_foot_ball
    revFootDico["heel"] = Rev_foot_heel
    
#     # make hierarchy
    revGrp.setParent(parentGrp)
    jointGrp, jointHlp = helpers.createOneHelper( sel = Rev_foot_ankle_start , freezeGrp = True, hierarchyParent = "insert")
    jointGrp.setParent(oneHlp)
    
    pm.parent(Rev_foot_heel, Rev_foot_ankle_start )
    Rev_foot_heel.setParent(Rev_foot_ankle_start)
    Rev_foot_end.setParent(Rev_foot_heel)
    Rev_foot_toes.setParent(Rev_foot_end)
    Rev_foot_free_toes.setParent(Rev_foot_end)
    Rev_foot_ball.setParent(Rev_foot_toes)
    Rev_foot_ankle_end.setParent(Rev_foot_ball)
    
    
    # make reverse foot system
        # add fk ctrls for rolling
    revfkRoot = fkChain.createFKchain(sel = [Rev_foot_heel, Rev_foot_end, Rev_foot_toes, Rev_foot_ball], collectHierarchy = False, rad = 3, axis=[0,1,0], hideSystem= False )
    revfkRoot[0].setParent(oneGrp)
    
        # add fk ctrl on additive toes joint
        
    # connect roll and angle attribute
    
    
    return oneGrp, Rev_foot_ankle_end, revFootDico, revfkRoot[0]



def createStretch(dico, parentGrp, rootJoint, ikEndJoint, mirroredJnt = False):
    """
    maj: 
    add follow joint
    add pole vector
    add override ctrl
    """
    print "start stretch"
    kneeJoint = rootJoint.getChildren()
    print(kneeJoint)
    print(kneeJoint[0].translateX.get())
    
    stretchGrp = pm.group(empty = True, name = "StretchFoot_grp")
    # create copy
    StretchRoot = pm.duplicate(rootJoint, name = (rootJoint.nodeName() + "_stretch_foot"), parentOnly = True)[0]
    StretchEnd = pm.duplicate(dico["ankle"], name = (dico["ankle"].nodeName() + "_stretch_foot"), parentOnly = True)[0]
    
    # make hierarchy
    stretchGrp.setParent(parentGrp)
    StretchRoot.setParent(stretchGrp)
    StretchEnd.setParent(StretchRoot)
    
    # align end of chain
    if mirroredJnt:
    # freeze joint
        pm.makeIdentity(StretchRoot, apply = True, t = False, r = True, s = False, n = False, pn = True)
        orientMirorredJoint(StretchRoot, StretchEnd)
    else:
        pass #classic orient
    
    StretchEnd.jointOrient.set([0.0, 0.0, 0.0])
    
    # make ik stretch system
    ikTmp = pm.ikHandle(startJoint= StretchRoot, endEffector= StretchEnd )
    ikHandle = ikTmp[0]
    
    # create ik strech control
    ctrlGrp, ctrl = helpers.createOneHelper(type = "circle", scale = 3, sel = ikHandle, axis = [0,1,0], freezeGrp= True, hierarchyParent= "insert" )
    ctrlGrp.rotate.set([0,0,0])
    
    if mirroredJnt:
        oneGrp, oneHelp = helpers.createOneHelper(sel = ctrl, freezeGrp= True, hierarchyParent= "insert" )
        oneGrp.rotate.set([0, 180, 180])
        
    ctrlGrp.setParent(stretchGrp)
    
    # stretch, roll, size, angle
    pm.addAttr(ctrl, ln="_______" , attributeType="enum", enumName="CTRLS:")
    pm.addAttr(ctrl, ln="stretch" , at='double', min=0, max=1, dv = 0)
    pm.addAttr(ctrl, ln="size" , at='double', min=-10, max=10, dv = 0)
    pm.addAttr(ctrl, ln="roll" , at='double', min=-5, max=10, dv = 0)
    pm.addAttr(ctrl, ln="angle" , at='double', min=-180, max=180, dv = 90)
    
    pm.setAttr(ctrl._______ , keyable=True, lock=True)
    pm.setAttr(ctrl.stretch , keyable=True)
    pm.setAttr(ctrl.size , keyable=True)
    pm.setAttr(ctrl.roll , keyable=True)
    pm.setAttr(ctrl.angle , keyable=True)
    
    ikHandle.setParent(ctrl)
    
    # add distance
    distGrp = pm.group(empty = True, parent = stretchGrp, name = "distance" )
    distNode, locs = helpers.creatDist(sel= [StretchRoot, ctrl ])
    distNode.setParent(distGrp)
    for l in locs:
        l.setParent(distGrp)
        
    
    #################### add stretch and size nodes and connections
        ####### size system
            # calculate leg_default_size (plusminus node)
    legSizeDef = pm.createNode("plusMinusAverage", name = "default_Leg_size")
                # connect original joint size to node
    pm.connectAttr(kneeJoint[0].translateX, legSizeDef.input1D[0])
    pm.connectAttr(ikEndJoint.translateX, legSizeDef.input1D[1])
    
    # if mirrored joint add multiply to negative size
    if mirroredJnt:
        legSizeDefInv = pm.createNode("multiplyDivide", name = "default_Leg_size_invert")
        legSizeDefInv.input2X.set(-1)
        pm.connectAttr(legSizeDef.output1D, legSizeDefInv.input1X)
        
    # create leg size condition (condition)
        # if current_leg_size (dist) < default_leg_size then return current_leg_size alse return default_leg_size
    resizeCond = pm.createNode("condition", name = "resize_leg_condition" )
    
    pm.connectAttr(distNode.distance, resizeCond.firstTerm )
    pm.connectAttr(legSizeDefInv.outputX, resizeCond.secondTerm )
    resizeCond.operation.set(5)
    
    pm.connectAttr(distNode.distance, resizeCond.colorIfTrueR )
    pm.connectAttr(legSizeDefInv.outputX, resizeCond.colorIfFalseR )
    
    # calculate additive leg_size (plusminus node)
        # connect size condition to node
    addSizeCond = pm.createNode("plusMinusAverage", name = "additive_leg_size" )
    pm.connectAttr(ctrl.size, addSizeCond.input1D[0] )
    pm.connectAttr(resizeCond.outColorR, addSizeCond.input1D[1] )
    
    # connect ik ctrl size to node
        # connect size addition to ik_end_joint translateX
    pm.connectAttr(addSizeCond.output1D, StretchEnd.translateX )
        
        ########## stretch system
    # create stretch_ratio_node (multiply divide/ divide mode)
        # connect current_leg_size to stretch_ratio_node input1X
        # connect leg_default_size or leg_default_size_invert to stretch_ratio_node input2X
    # create plusminus node to calculate stretch additive
    # create multiplydivide node to mutiply stretch additive with stretch attribute
    # create plusminus node to calculate final stretch
    # create condition to apply stretch only when stretch > 1
    
    print "end stretch"
    return stretchGrp, StretchRoot, StretchEnd, ctrl
    

############################################## MAIN ############################ 
"""
maj:
 -- def to find potential reverse foot in scene
 -- apply reverse foot from ankle. ignore L and R distinction. only mirrored joint param.
"""


# sel = pm.ls(sl = True)
sel = pm.ls(pm.PyNode("body_jnt"))

# create hierarchy
motionGrp = SRD.initMotionSystem ()
defGrp = SRD.initDeformSystem ()

# find foot joint
R_foot_dict, L_foot_dict = findFeet(sel)

revFootGrp = None

# create reverse foot grp
res = pm.ls('reverse_foot_grp')
if len(res) == 0: 
    revFootGrp = pm.group(empty = True, name = "reverse_foot_grp")
    revFootGrp.setParent(motionGrp)
else:
    revFootGrp = res[0]

pprint (R_foot_dict)
pprint (L_foot_dict)

switchCtrl = None
ikRoot = None
ikCtrl = None
joinTarget = []
ikEndJoint = None
fkEndJoint = None

# find 
# find ik root, ik switch, 
if L_foot_dict.has_key("ankle"): switchCtrl, ikRoot, ikCtrl, jointTarget, ikEndJoint, fkEndJoint = initChain(L_foot_dict)

## create fk foot chain
fkFootChain, fkFootDico, fkRoot = createFKFoot(L_foot_dict, revFootGrp )

## create ik stretch chain
stretchGrp, StretchRoot, StretchEnd, StretchCtrl = createStretch(L_foot_dict,revFootGrp, ikRoot, mirroredJnt= True, ikEndJoint = ikEndJoint )

## create reverse foot chain
revFootStart, revFootEnd, revFootDico, revRootCtrl  = createReverseFoot(L_foot_dict, revFootGrp, StretchCtrl)

# parent fk foot system to fk leg system(no alias)
    # parent fk foot start(grp) to joint or ctrl? joint
pm.parentConstraint(fkEndJoint, fkRoot)
pm.scaleConstraint(fkEndJoint, fkRoot)

# parent reverse foot system to ik strech system(no alias)
    # parent reverse foot root joint on ik stretch
pm.pointConstraint(StretchEnd, revFootStart)
pm.orientConstraint(StretchCtrl, revFootStart)
# pm.parentConstraint(StretchCtrl, revRootCtrl)

# parent ik leg system to reverse foot system(ctrl to ankle joint)
pm.pointConstraint(revFootEnd, ikCtrl.getParent())
    # lock autostrech and followctrl



# parent foot deformation system to fk and ik feet
pprint(fkFootDico)
pprint(L_foot_dict)
pprint(revFootDico)

for attr in ["end", "ball", "heel", "toes"]:
    parentConst = pm.parentConstraint(fkFootDico[attr], revFootDico[attr], L_foot_dict[attr])
    targetsList = pm.parentConstraint(parentConst, query = True, weightAliasList  = True)
    # connect parents constraints to ikfkSwitch
    for t in targetsList:
        if "FK" in t.name():
            print(t)
            pm.connectAttr(switchCtrl.fk, t, f = True)
        elif "Rev" in t.name():
            print(t)
            pm.connectAttr(switchCtrl.ik, t, f = True)
       
    scaleConst = pm.scaleConstraint(fkFootDico[attr], revFootDico[attr], L_foot_dict[attr])
    scaleTargetsList = pm.scaleConstraint(scaleConst, query = True, weightAliasList  = True)
    # connect parents constraints to ikfkSwitch
    for s in scaleTargetsList:
        if "FK" in s.name():
#             print(t)
            pm.connectAttr(switchCtrl.fk, s, f = True)
        elif "Rev" in s.name():
#             print(t)
            pm.connectAttr(switchCtrl.ik, s, f = True)

# manage visibility