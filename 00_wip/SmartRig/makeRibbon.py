
import pymel.core as pm
import maya.mel as mm

import pymel.core.nodetypes as nt

import maya.OpenMaya as om
import maya.OpenMayaUI as omui

def createPlane(sections = 3):
    sel = pm.ls(sl = True)[0]
    
    selChild = sel.listRelatives(c = True, typ = 'joint')[0]
    planSize = selChild.translateX.get()
    
    onePlan = pm.nurbsPlane(ch = False, o = True, po = False, ax = [0,1,0], w = planSize, lr = 0.25, u = sections, name = 'ribbon_plane')
    onePlan[0].setParent(sel)
    onePlan[0].translate.set([planSize/2,0,0])
    onePlan[0].rotate.set([0,0,0])
    pm.parent(onePlan, w = True)
    
def makeRibbon(jointSize = 0.2):
        
    # CREATION DU RIBBON
    # recup de la selection
    multiSel = pm.ls(sl= True)
    
    for sel in multiSel:
        # recup de la shape
        planeShapeStr = sel.getShape()
    
    #     num patch
        folNum =  planeShapeStr.spansU.get()
        
        var = folNum
        part = 1.0/var
        uValue = 0
        folList = []
        
    #     follicles creation
        for i in range(var):
            
            minU = uValue
            uValue = uValue + part
            maxU = uValue
            midU = (minU + maxU)*0.5
        
            fol= pm.createNode('follicle')
            folParent =  fol.getParent()
            pm.rename(folParent, '%s_follicle_%s' % (sel.nodeName(), i))
                
            pm.connectAttr('%s.local' % sel.getShape(), '%s.inputSurface' % fol)
            pm.connectAttr('%s.worldMatrix[0]' % sel.getShape(), '%s.inputWorldMatrix' % fol)
            pm.connectAttr('%s.outRotate' % fol, '%s.rotate' %  fol.getParent())
            pm.connectAttr('%s.outTranslate' % fol, '%s.translate' % fol.getParent())
            
            # center Object On Plane
            pm.setAttr("%s.parameterU" % fol.nodeName(), midU)
            pm.setAttr("%s.parameterV" % fol.nodeName(), 0.5)
            
            folList.append(folParent)
            
    #     curveList creation
        curveList = []
        for fol in folList:
            oneGroup = pm.group(em = True, name = ( fol.nodeName() + "_grp" ))
            oneGroup.setParent(fol)
            oneGroup.translate.set([0,0,0])
            oneGroup.rotate.set([0,0,0])
            oneGroup.scale.set([1,1,1])
            curveList.append(oneGroup)
        
         #creer les joints associer aux follicles et les parenter
        deformJointsList = []
        for i,curve in enumerate(curveList):
            jointTemp = pm.joint(n = "%s_joint_%s" % (curve, i), rad = jointSize)
            jointTemp.setParent(curve)
            jointTemp.translate.set([0,0,0])
            jointTemp.jointOrient.set([0,0,0])
            deformJointsList.append(jointTemp)
        
        # CREATION DU RIG    
        # recuperation de la taille du ribbon
        ribbonLength, ribbonWidth = ribbonSize(sel)
        
        # positionnement du loc central
        locOne = pm.spaceLocator(n = (sel.name() + "_twist"))
        locOne.setParent(sel)
        locOne.translate.set([0,0,0])
        locOne.rotate.set([0,0,0])
        
        # positionnement du loc up
        locTwo = pm.duplicate(locOne, n = (sel.name() + "_twist_up") )[0]
        locTwo.translateX.set(ribbonLength/2)
        
        # positionnement du loc down
        locThree = pm.duplicate(locOne, n = (sel.name() + "_twist_down") )[0]
        locThree.translateX.set(ribbonLength/2*-1)
        
        locList = [ locTwo, locOne,  locThree ]
    
        allLocList = []
        
        # creation des arbres
        for obj in locList:
            Aim = pm.duplicate(obj, n = (obj.name() + "_aim") )[0]
            Up = pm.duplicate(obj, n = (obj.name() + "_up") )[0]
            
            Aim.setParent(obj)
            Up.setParent(obj)
            
            Up.translateY.set(10)
            
            pm.parent(obj, w = True )
            
            allLocList.append( obj )
            allLocList.append( Aim )
            allLocList.append( Up )
            
        # creation des joints pour le skin du ribbon
            
        jointSkinList = []
        
        for i in range(1,10,3):
    #         print allLocList[i]
            jointOne = pm.joint(n = (allLocList[i].name() + "_joint"), rad = jointSize*1.5)
            jointOne.setParent(allLocList[i])
            jointOne.translate.set([0,0,0])
            jointOne.jointOrient.set([0,0,0])
            jointSkinList.append(jointOne)
        
        jointEndList = []
        
        for i in range(0,3,2):
            print jointSkinList[i]
            jointTwo = pm.duplicate(n = jointSkinList[i].name())[0]
            jointTwo.setParent(jointSkinList[i])
            jointTwo.translate.set([0,0,0])
            jointTwo.translateX.set(1)
            jointEndList.append(jointTwo)
        
        # creation des contraintes
        pm.aimConstraint(jointSkinList[1] , allLocList[1], wut = "object", wu = [0,1,0], wuo = allLocList[2]  )
        pm.aimConstraint(jointSkinList[1] , allLocList[7], wut = "object", wu = [0,1,0], wuo = allLocList[8]  )
        pm.pointConstraint(allLocList[6],allLocList[0], allLocList[3])
        pm.pointConstraint(allLocList[8],allLocList[2], allLocList[5])
        
        pm.aimConstraint(allLocList[6] ,allLocList[4], wut = "object", wu = [0,1,0], wuo = allLocList[5]  )
        
        # ccreation du skin
        pm.skinCluster( jointSkinList[0], jointSkinList[1], jointSkinList[2], jointEndList[0], jointEndList[1], sel)
        
    #     organize tree
        motionSysGrp = pm.group (em = True, name = ( '%s_motion_system' % (sel.nodeName())))
        pm.parent(locList,motionSysGrp )
    
        deformSysGrp = pm.group (em = True, name = ( '%s_deform_system' % (sel.nodeName())))
        pm.parent(folList,deformSysGrp )
        
        ribbonSysGrp = pm.group (em = True, name = ( '%s_system' % (sel.nodeName())))
        pm.parent(sel, ribbonSysGrp)
        pm.parent(motionSysGrp, ribbonSysGrp)
        pm.parent(deformSysGrp, ribbonSysGrp)
    
def ribbonSize(sel):
    cvList =  sel.getCVs()
    minX = cvList[0][0]
    maxX = cvList[0][0]
    minZ = cvList[0][2]
    maxZ = cvList[0][2]
    
    for cv in cvList:
    
        if cv[0]<minX:
            print(cv[0], minX)
            minX = cv[0]
            print(minX)
        if cv[0]>maxX:
            maxX = cv[0]
            
        if cv[2]<minZ:
            minZ = cv[2]
        if cv[2]>maxZ:
            maxZ = cv[2]
            
            
    lenght = maxX - minX
    width = maxZ - minZ
    om.MGlobal_displayInfo('ribbon lenght: \t%s \tribbon width: \t%s' % (lenght, width))
    return(lenght, width)

