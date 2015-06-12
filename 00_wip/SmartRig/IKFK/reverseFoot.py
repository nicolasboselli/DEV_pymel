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
reload(helpers)

def defineFootStructure(sel = None):
    # test ankle selection
    if not sel.getAttr("type") == 18 and not sel.getAttr("otherType") == "ankle":
        om.MGlobal_displayWarning("bad selection")
        return
    
    # collect ankle
    print sel
    footDict = {}
    allJnt = pm.listRelatives(sel, allDescendents = True, type= "joint")
    allJnt.append(sel)
    
    for j in allJnt:
        if(j.getAttr("type") == 18):
            print(j.getAttr("otherType"))
            if (j.getAttr("otherType") == "ankle"):
                footDict["ankle"] = j
            elif (j.getAttr("otherType") == "end"):
                footDict["end"] = j
            elif (j.getAttr("otherType") == "toes"):
                footDict["toes"] = j
            elif (j.getAttr("otherType") == "ball"):
                footDict["ball"] = j
            elif (j.getAttr("otherType") == "heel"):
                footDict["heel"] = j
                
    return footDict
"""
sel = pm.ls(sl = True)[0]
footDict = defineFootStructure(sel = sel)
pprint(footDict)
"""

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
    revfkRoot, revfkCtrlsGrp, revfkCtrls = fkChain.createFKchain(sel = [Rev_foot_heel, Rev_foot_end, Rev_foot_toes, Rev_foot_ball], collectHierarchy = False, rad = 3, axis=[0,1,0], hideSystem= False, returnCtrls= True )
    revfkRoot[0].setParent(oneGrp)
    
        # add fk ctrl on additive toes joint
    
        
        
    ########## create roll
        # connect roll and angle attribute
            # heel grp connection 
                # create condition
    heel_rolling_condition = pm.createNode("condition", name = "heel_rolling_condition")
    pm.connectAttr(stretchCtrl.roll, heel_rolling_condition.firstTerm)
    pm.connectAttr(heel_rolling_condition.firstTerm, heel_rolling_condition.colorIfTrueR)
    heel_rolling_condition.colorIfFalseR.set(0)
    heel_rolling_condition.operation.set(5)
    
                # create multiplydivide "regul"
    heel_rolling_regul = pm.createNode("multiplyDivide", name = "heel_rolling_regul")
    pm.connectAttr(heel_rolling_condition.outColorR, heel_rolling_regul.input1X)
    heel_rolling_regul.input2X.set(-0.2)
    
                # create mutiplydivide "angle"
    heel_rolling_angle = pm.createNode("multiplyDivide", name = "heel_rolling_angle")
    pm.connectAttr(stretchCtrl.angle, heel_rolling_angle.input1X)
    pm.connectAttr(heel_rolling_regul.outputX, heel_rolling_angle.input2X)
    
                # freeze grp
    helpGrp, help = helpers.createOneHelper(sel = revfkCtrlsGrp[0],  freezeGrp = False, hierarchyParent = "insert")
                # connect to group
    pm.connectAttr(heel_rolling_angle.outputX, revfkCtrlsGrp[0].rotateY)
    
            # end connection 
                # create plus minus
    end_rolling_minore = pm.createNode("plusMinusAverage", name = "end_rolling_minore")
    pm.connectAttr(stretchCtrl.roll, end_rolling_minore.input1D[0])
    end_rolling_minore.input1D[1].set(5)
    end_rolling_minore.operation.set(2)
                # create condition
    end_rolling_condition = pm.createNode("condition", name = "end_rolling_condition")
    pm.connectAttr(stretchCtrl.roll, end_rolling_condition.firstTerm)
    pm.connectAttr(end_rolling_minore.output1D, end_rolling_condition.colorIfTrueR)
    end_rolling_condition.colorIfFalseR.set(0)
    end_rolling_condition.secondTerm.set(5)
    end_rolling_condition.operation.set(2)
    
                # create multiplydivide "regul"
    end_rolling_regul = pm.createNode("multiplyDivide", name = "end_rolling_regul")
    pm.connectAttr(end_rolling_condition.outColorR, end_rolling_regul.input1X)
    end_rolling_regul.input2X.set(-0.2)
                
                # create mutiplydivide "angle"
    end_rolling_angle = pm.createNode("multiplyDivide", name = "end_rolling_angle")
    pm.connectAttr(stretchCtrl.angle, end_rolling_angle.input1X)
    pm.connectAttr(end_rolling_regul.outputX, end_rolling_angle.input2X)
                # freeze grp
    helpGrp, help = helpers.createOneHelper(sel = revfkCtrlsGrp[1],  freezeGrp = False, hierarchyParent = "insert")
                # connect ro group
    pm.connectAttr(end_rolling_angle.outputX, revfkCtrlsGrp[1].rotateY)
                
                
            # ball connection 
                # create condition
    ball_rolling_first_condition = pm.createNode("condition", name = "ball_rolling_first_condition")
    pm.connectAttr(stretchCtrl.roll, ball_rolling_first_condition.firstTerm)
    pm.connectAttr(ball_rolling_first_condition.firstTerm, ball_rolling_first_condition.colorIfTrueR)
    ball_rolling_first_condition.operation.set(2)
    ball_rolling_first_condition.colorIfFalseR.set(0)
    
                # create plus minus
    ball_rolling_minore = pm.createNode("plusMinusAverage", name = "ball_rolling_minore")
    ball_rolling_minore.input1D[0].set(10)
    pm.connectAttr(ball_rolling_first_condition.outColorR, ball_rolling_minore.input1D[1])
    ball_rolling_minore.operation.set(2)
    
                # create condition
    ball_rolling_second_condition = pm.createNode("condition", name = "ball_rolling_second_condition")
    pm.connectAttr(ball_rolling_first_condition.outColorR, ball_rolling_second_condition.firstTerm)
    pm.connectAttr(ball_rolling_minore.output1D, ball_rolling_second_condition.colorIfFalseR)
    pm.connectAttr(ball_rolling_second_condition.firstTerm, ball_rolling_second_condition.colorIfTrueR)
    ball_rolling_second_condition.operation.set(4)
    ball_rolling_second_condition.secondTerm.set(5)
    
                # create multiplydivide "regul"
    ball_rolling_regul = pm.createNode("multiplyDivide", name = "ball_rolling_regul")
    pm.connectAttr(ball_rolling_second_condition.outColorR, ball_rolling_regul.input1X)
    ball_rolling_regul.input2X.set(-0.2)
    print "check 6"
                # create mutiplydivide "angle"
    ball_rolling_angle = pm.createNode("multiplyDivide", name = "ball_rolling_angle")
    pm.connectAttr(stretchCtrl.angle, ball_rolling_angle.input1X)
    pm.connectAttr(ball_rolling_regul.outputX, ball_rolling_angle.input2X)
                # freeze grp
    helpGrp, help = helpers.createOneHelper(sel = revfkCtrlsGrp[2],  freezeGrp = False, hierarchyParent = "insert")
                # connect ro group
    print "check 35"
    pm.connectAttr(ball_rolling_angle.outputX, revfkCtrlsGrp[2].rotateY)
    print "check 4"
    
    
    return oneGrp, Rev_foot_ankle_end, revFootDico, revfkRoot[0], revfkCtrlsGrp



def createStretch(dico, parentGrp, rootJoint, ikEndJoint, mirroredJnt = False):
    """
    maj: 
    add follow joint
    add pole vector
    add override ctrl
    """
    kneeJoint = rootJoint.getChildren()
    
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
    
    legSizeDefInv = None
    # if mirrored joint add multiply to negative size
    
    if mirroredJnt:
        legSizeDefInv = pm.createNode("multiplyDivide", name = "default_Leg_size_invert")
        legSizeDefInv.input2X.set(-1)
        pm.connectAttr(legSizeDef.output1D, legSizeDefInv.input1X)
        
    # create leg size condition (condition)
        # if current_leg_size (dist) < default_leg_size then return current_leg_size alse return default_leg_size
    resizeCond = pm.createNode("condition", name = "resize_leg_condition" )
    
    pm.connectAttr(distNode.distance, resizeCond.firstTerm )
    # if mirroredJoint
    if mirroredJnt:
        pm.connectAttr(legSizeDefInv.outputX, resizeCond.secondTerm )
    else:
        pm.connectAttr(legSizeDef.output1D, resizeCond.secondTerm )
        
    resizeCond.operation.set(5)
    
    pm.connectAttr(distNode.distance, resizeCond.colorIfTrueR )
    # if mirroredJoint
    if mirroredJnt:
        pm.connectAttr(legSizeDefInv.outputX, resizeCond.colorIfFalseR )
    else:
        pm.connectAttr(legSizeDef.output1D, resizeCond.colorIfFalseR )
        
    
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
    stretch_ratio_node = pm.createNode("multiplyDivide", name = "stretch_ratio_node")
    stretch_ratio_node.operation.set(2)
        # connect current_leg_size to stretch_ratio_node input1X
    pm.connectAttr(distNode.distance, stretch_ratio_node.input1X)
    
        # connect leg_default_size or leg_default_size_invert to stretch_ratio_node input2X
    if mirroredJnt:
        pm.connectAttr(legSizeDefInv.outputX, stretch_ratio_node.input2X)
    else:
        pm.connectAttr(legSizeDef.output1D, stretch_ratio_node.input2X)
    
    # create plusminus node to calculate stretch additive
    stretch_add = pm.createNode("plusMinusAverage", name = "stretch_additive")
    pm.connectAttr(stretch_ratio_node.outputX, stretch_add.input1D[0])
    stretch_add.input1D[1].set(1)
    stretch_add.operation.set(2)
    
    # create multiplydivide node to mutiply stretch additive with stretch attribute
    stretch_multiply = pm.createNode("multiplyDivide", name = "stretch_multiply")
    pm.connectAttr(stretch_add.output1D, stretch_multiply.input1X)
    pm.connectAttr(ctrl.stretch, stretch_multiply.input2X)
    
    # create plusminus node to calculate final stretch
    stretch_final = pm.createNode("plusMinusAverage", name = "stretch_final")
    stretch_final.input1D[0].set(1)
    pm.connectAttr(stretch_multiply.outputX, stretch_final.input1D[1])
    
    # create condition to apply stretch only when stretch > 1
    stretch_condition = pm.createNode("condition", name = "stretch_condition")
    pm.connectAttr(stretch_final.output1D, stretch_condition.firstTerm)
    pm.connectAttr(stretch_condition.firstTerm, stretch_condition.colorIfTrueR)
    stretch_condition.secondTerm.set(1)
    stretch_condition.operation.set(3)
    
    # connect to joint
    pm.connectAttr(stretch_condition.outColorR, StretchRoot.scaleX )
    
    
    print "end stretch"
    return stretchGrp, StretchRoot, StretchEnd, ctrl, distNode, legSizeDefInv
    

def createRevFoot(sel = None, mirroredJnt = False):
    """
    maj: anchor
    """
    # create hierarchy
    motionGrp = SRD.initMotionSystem ()
    defGrp = SRD.initDeformSystem ()
    
    # test the selection
    # return foot dictionnary from ankle selection
    foot_dict = defineFootStructure(sel)
    # find ik root, ik switch, 
    if foot_dict.has_key("ankle"): switchCtrl, ikRoot, ikCtrl, jointTarget, ikEndJoint, fkEndJoint = initChain(foot_dict)
    
    # create reverse foot grp
    revFootGrp = None
    tmpName = sel.nodeName() + "_reverse_foot_grp"
    res = pm.ls(tmpName)
    if len(res) == 0: 
        revFootGrp = pm.group(empty = True, name = tmpName)
        revFootGrp.setParent(motionGrp)
    else:
        revFootGrp = res[0]
    
    ## create fk foot chain
    fkFootChain, fkFootDico, fkRoot = createFKFoot(foot_dict, revFootGrp )
    
    ## create ik stretch chain
    stretchGrp, StretchRoot, StretchEnd, StretchCtrl, distNode, legSizeDef = createStretch(foot_dict,revFootGrp, ikRoot, mirroredJnt= mirroredJnt, ikEndJoint = ikEndJoint )
    
    ## create reverse foot chain
    revFootStart, revFootEnd, revFootDico, revRootCtrl, revfkCtrlsGrp  = createReverseFoot(foot_dict, revFootGrp, StretchCtrl)
    
    
    
    ### parent fk foot system to fk leg system(no alias)
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
    
    
    
    ### parent foot deformation system to fk and ik feet
    for attr in ["end", "ball", "heel", "toes"]:
        parentConst = pm.parentConstraint(fkFootDico[attr], revFootDico[attr], foot_dict[attr])
        targetsList = pm.parentConstraint(parentConst, query = True, weightAliasList  = True)
        # connect parents constraints to ikfkSwitch
        for t in targetsList:
            if "FK" in t.name():
                print(t)
                pm.connectAttr(switchCtrl.fk, t, f = True)
            elif "Rev" in t.name():
                print(t)
                pm.connectAttr(switchCtrl.ik, t, f = True)
           
        scaleConst = pm.scaleConstraint(fkFootDico[attr], revFootDico[attr], foot_dict[attr])
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
    

############################################## MAIN ############################ 

"""
maj:
 -- def to find potential reverse foot in scene
 -- apply reverse foot from ankle. ignore L and R distinction. only mirrored joint param.
"""


sel = pm.ls(sl = True)[0]
# sel = pm.ls(pm.PyNode("body_jnt"))
createRevFoot(sel = sel, mirroredJnt= False)
