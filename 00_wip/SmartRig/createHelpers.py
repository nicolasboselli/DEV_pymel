#-*- coding: utf-8 -*

'''
Created on 13 déc. 2013

@author: nico
'''
import pymel.core as pm
import maya.mel as mm
import maya.OpenMaya as om

"""
maj:
    parent circle as option
    find joints children in hierarchy as option
    set circle size
"""
def createCircle(axis, sel = None, findHierarchy = False, parentHierachy = False, radius = 2):
    if not sel:
        sel = pm.ls(sl = True)
    
    circles = []
    
    for s in sel:
        oneCircle = pm.circle(n = (s.nodeName() + "_ctrl"), ch = False, o = True, nr = axis, r = radius)[0]
        oneGroup = pm.group(em = True, name = ( oneCircle.nodeName() + "_grp" ))
        
        oneCircle.setParent(oneGroup)
        pm.parent(oneGroup, s, r = True)
        pm.parent(oneGroup, w = True)
        
        om.MGlobal_displayInfo('circle created: \t%s' % oneCircle.nodeName())
        circles.append(oneCircle)
        
    om.MGlobal_displayInfo('circle creation done')
    return(circles)

def rootGroup(sel = None):
    if not sel:
        sel = pm.ls(sl = True)
    rootGrps = []
    
    for s in sel:
        oneGroup = pm.group(em = True, name = ( s.name() + "_null" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
        pm.parent(oneGroup, w = True)
        s.setParent(oneGroup)
        
        rootGrps.append(oneGroup)
        
    return(rootGrps)

def insertGroup():
    sel = pm.ls(sl = True)
    for s in sel:
        bakParent = s.getParent()
        oneGroup = pm.group(em = True, name = ( s.name() + "_null" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
        pm.parent(oneGroup, w = True)
        s.setParent(oneGroup)
        oneGroup.setParent(bakParent)

def childGroup():
    sel = pm.ls(sl = True)
    for s in sel:
        oneGroup = pm.group(em = True, name = ( s.name() + "_null" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
def createLoc(rad):    
    sel = pm.ls(sl = True)
    for s in sel:
        oneLoc = pm.spaceLocator(a = True, name = (s.name() + "_loc") )
        oneLoc.localScale.set([rad,rad,rad])
        pm.parent(oneLoc, s, r = True)
        pm.parent(oneLoc, w = True)
    
def creatDist(sel = None):
    if not sel:
        sel = pm.ls(sl = True)
        
    if len(sel) == 2:
        distNodeShape = pm.distanceDimension(sp = [0,0,0], ep = [0,50,0])
        distNode = pm.listRelatives(distNodeShape, fullPath = True, parent = True)
        locs = pm.listConnections(distNodeShape, s = True)
        
        pm.rename(locs[0], (sel[0].name() + "_dist_loc1"))
        pm.rename(locs[1], (sel[1].name() + "_dist_loc2"))
        pm.rename(distNode, (sel[0].name() + "_dist"))
        
        pm.pointConstraint(sel[1], locs[1], w = True)
        pm.pointConstraint(sel[0], locs[0], w = True)
        
        return distNodeShape, locs
    else:
        om.MGlobal_displayError('non conform selection')
 