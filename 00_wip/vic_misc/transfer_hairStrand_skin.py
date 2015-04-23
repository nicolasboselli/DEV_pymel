'''
Created on 3 dec. 2014

@author: gamma project
'''

import os, sys

import maya.mel as mel

from PySide import QtCore
from PySide import QtGui
import pymel.core as pm

from pprint import pprint

import re

## ===============================================================================creating name matching dictionnary 
'''
# get reference curves names
curvRoot = pm.PyNode('Geometry|Hair_reduced_Curves')
curvRef = pm.listRelatives(curvRoot, children = True, fullPath  = True)
for cr in curvRef:
    print(cr.nodeName())

# get new curves
curvNew = pm.PyNode('hair_new|Hair_reduced_Curves')
curvsNew = pm.listRelatives(curvNew, children = True)
for cn in curvsNew:
    print(cn.nodeName())

# get new curves
curvFilled = pm.PyNode('hair_new|Hair_reduced_fillerCurves')
curvsFiller = pm.listRelatives(curvFilled, children = True)
for cn in curvsFiller:
    print(cn.nodeName())
    
# backup oldName, newName)
matchName = {}
for i,name in enumerate(curvRef):
    matchName[curvsNew[i].nodeName()] = curvRef[i].nodeName()
print(matchName)

# save match name dico
f = r'C:\matchNameDict.txt'

destHandle = open(f,'w')
destHandle.writelines(str(matchName))
destHandle.close()
'''

######################### Start Step 1: clean hair curves import
## ========================================================================= warning: make clean shape before match skin
##    ======================================================================= delete follicule
roots = pm.ls(sl = True)
for t in roots:
    children = pm.listRelatives(t, allDescendents = True, type = 'follicle')
    for c in children:
        pm.delete(c)


## ============================================================================renaming curve with dico reference
# manual: rename CUrves_22 to Curves_30

hairNew = pm.PyNode('hair_new')

# get new curves
curvNew = pm.PyNode('hair_new|Hair_reduced_Curves')
curvsNew = pm.listRelatives(curvNew, children = True)
for cn in curvsNew:
    print(cn.nodeName())

# get new curves
curvFilled = pm.PyNode('hair_new|Hair_reduced_fillerCurves')
curvsFiller = pm.listRelatives(curvFilled, children = True)
for cn in curvsFiller:
    print(cn.nodeName())

# load matchName dico
f = r'C:\matchNameDict.txt'
sourceHandle = open(f, 'r').read()
matchNames = eval(sourceHandle)
pprint(matchNames)

    
# change name in 'Hair_reduced_Curves' by order of creation
for c in curvsNew:
    search = c.nodeName()
    if search in matchNames.keys():
        pm.rename(c, matchNames[search] )
        print(search, matchNames[search])
        
        
# change name in 'Hair_reduced_fillerCurves' by order of creation
for key in matchNames.keys():
    for c in curvsFiller:
        if key in c.nodeName():
            pm.rename(c, matchNames[key])
            print(c.nodeName(), 'filler%s' % matchNames[key])

# rename 'hairNew'
pm.rename(hairNew, 'hair_curves')
# reparent 'hairNew
pm.parent(hairNew, 'Geometry')

######################### End Step 1: clean hair curves import




# =========================================================================== manual: execute quentin skinPaster first


######################### Start step 2: transfer skin cluster on curves
## ==========================================================================script for skin transfer on hair curves
## script for curves renaming

# get curves grp relatives list
rootCurves = pm.PyNode("hair_curves|Hair_reduced_Curves")
rootFillerCurves = pm.PyNode("hair_curves|Hair_reduced_fillerCurves")

children = pm.listRelatives(rootCurves, children = True, type = 'transform')
FillerChildren = pm.listRelatives(rootFillerCurves, children = True, type = 'transform')

children = children + FillerChildren

# find hairstrand grp relatives list
hairMeshes = pm.ls("head_grp|hair_grp")
hairStrandList = pm.listRelatives(hairMeshes, children = True)


# find matching curves grp and hairstrand meshes
for c in children:
    for m in hairStrandList:
        mName = m.nodeName()
        cName = c.nodeName()
#         print(cName, mName)
        if mName in cName:
            print(mName, cName)
            curves = pm.listRelatives(c, allDescendents = True, type = 'nurbsCurve')
            print(curves)
            for curv in curves:
                pm.select(m, curv)
                # transfer mesh skin on curves
                mel.eval('qa_matchInfluences')
                mel.eval('qa_launchMayaCopySkinWeightsBtwn2Objs')

######################### end step 2: transfer skin cluster on curves



## =========================================================================script for hair curve blend shape  creation
# duplicate hair curves grp
curveToWrap = pm.duplicate(hairNew, name = hairNew.nodeName() + '_toWrap')
print'copy done'

# children = pm.listRelatives(curveToWrap, children = True, type = 'transform')

# get hairCurves group
rootCurves = pm.PyNode("hair_curves_toWrap|Hair_reduced_Curves")
rootFillerCurves = pm.PyNode("hair_curves_toWrap|Hair_reduced_fillerCurves")

children = pm.listRelatives(rootCurves, children = True, type = 'transform')
FillerChildren = pm.listRelatives(rootFillerCurves, children = True, type = 'transform')

children = children + FillerChildren


# find hairstrand grp relatives list
hairStrandList = pm.listRelatives(hairMeshes, children = True)
# pprint(hairStrandList)


# find matching curves grp and hairstrand meshes

# wrap each curve with relative mesh
for c in children:
    for m in hairStrandList:
        mName = m.nodeName()
        cName = c.nodeName()
#         print(cName, mName)
        if mName in cName:
            pm.select(c, m)
            pm.runtime.CreateWrap()

# ========================================================================= manual: create blendshape
# active blendshape on mesh
# delete history on curve
# delete copy of hairStrand meshes created for the wrap

# ========================================================================= manual: correct blendshape with ponderate cvs

## ============================================================================= ponderate cvs selected
def ponderateCVS():
    cvs = pm.ls(sl = True)
    print(cvs)
    for cv in cvs:
        # get cv curve
        splitName = cv.split('|')
        gap = '|'
        count = len(splitName)
        pasteList = []
        for i in range(count-1):
            pasteList.append(splitName[i])
        curveName = gap.join(pasteList)
        curve = pm.PyNode(curveName)
        print(curve)
        
        # get cv index
        numBase = cv.split('.cv')[-1]
        numBase = numBase.replace('[','')
        numBase = numBase.replace(']','')
        
        # get cv list
        numList = []
        if ':' in numBase:
            numListTmp = numBase.split(':')
            preNumList = []
            for n in numListTmp:
                preNumList.append(int(n))
                
            preNumList = sorted(preNumList)
            for i in range(preNumList[0],(preNumList[1] + 1)):
                numList.append(i)
                
        else:
            numList.append(int(numBase))
        
        for numCv in numList: 
            
            # get pre point
            prePt = curve.getCV(numCv - 1)
            # get post point
            postPt = curve.getCV(numCv + 1)
            
            # calculate median position
            newPos = [(prePt[0] + postPt[0])/2, (prePt[1] + postPt[1])/2, (prePt[2] + postPt[2])/2]
            print(prePt,newPos, postPt)
            
            # apply new position
            curve.setCV(numCv, newPos)
            curve.updateCurve()

ponderateCVS()



############################################################################ start step 3: blenshape connection
# ========================================================================= connect blendshape
# rename blendshape
pm.rename(curveToWrap, 'hair_curves_bs' )
# parent blendshape on blendshape 
pm.parent(curveToWrap, 'blendshapes')
# hide blendshape
for c in curveToWrap:
    pm.setAttr('%s.visibility' % c.name(), 0)
# create blendshape on curve by group
blendNode = pm.blendShape(curveToWrap, hairNew, frontOfChain = True, name = "BS_hair_curves" )
print(blendNode)
# connect to controller
pm.connectAttr('M_head_up_02_ctrl.HairPop', '%s.hair_curves_bs' % blendNode[0].nodeName())
############################################################################ start step 3: blenshape connection

############################################################################ start step 4: connect squash and stretch
## ======================================================================== apply squash and stretch
headSquash = pm.ls('head_squash_Handle', r = 1)[0]
headBendRL = pm.ls('bend_headRL_Handle', r = 1)[0]
headBendFB = pm.ls('bend_headFB_Handle', r = 1)[0]

toSquashCurves = pm.PyNode('hair_curves')


pm.nonLinear(headSquash, e = True, g = toSquashCurves)
pm.nonLinear(headBendRL, e = True, g = toSquashCurves)
pm.nonLinear(headBendFB, e = True, g = toSquashCurves)
############################################################################ end step 4: connect squash and stretch


## ========================================================================= select curves to geocacheset (bake4hair)
setTmp = pm.listRelatives('hair_curves', allDescendents  = True, type = 'transform')
geoCacheSet = []
for elt in setTmp:
    if elt.getShape():
        geoCacheSet.append(elt)
        
pm.select(geoCacheSet)



    
