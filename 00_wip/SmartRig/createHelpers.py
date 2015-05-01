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
    set circle size
    create circle by createOneHelpers
"""
def createCircle(axis, sel = None, radius = 2, suffix = "_ctrl"):
    if not sel:
        sel = pm.ls(sl = True)
    
    circles = []
    circlesGrp = []
    
    for s in sel:
        oneGroup, oneCircle = createOneCircle(axis, sel = s, rad = radius, suf = suffix )

        circlesGrp.append(oneGroup)
        circles.append(oneCircle)
        
    om.MGlobal_displayInfo('circle creation done')
    print"check 3"
    return(circlesGrp, circles)

def createOneCircle(axis, sel = None, rad = 2, suf = "_ctrl"):
    oneCircle = pm.circle(n = (sel.nodeName() + suf), ch = False, o = True, nr = axis, r = rad)[0]
    oneGroup = pm.group(em = True, name = ( oneCircle.nodeName() + "_grp" ))
    
    oneCircle.setParent(oneGroup)
    pm.parent(oneGroup, sel, r = True)
    pm.parent(oneGroup, w = True)
    
    om.MGlobal_displayInfo('circle created: \t%s' % oneCircle.nodeName())   
    print "check 4"
    return oneGroup,oneCircle

def createOneHelper(type, axis = [0,1,0], sel = None, scale = 1, suf = ""):
    oneHelp = None
    if type == "cube":
        oneHelp = createOneCube(d = scale, sel = sel)
    elif type == "cross":
        oneHelp = createCross(d = scale)
    elif type == "sphere":
        pass
    elif type == "circle":
        pass
    elif type == "square":
        pass
    
    if not oneHelp: 
        om.MGlobal_displayError('type error')   
        return
    
    if sel: pm.rename(oneHelp, (sel.nodeName() + suf + "_crtl"))
    
    oneGroup = pm.group(em = True, name = (oneHelp.nodeName() + "_grp" ))
    oneHelp.setParent(oneGroup)
    pm.parent(oneGroup, sel, r = True)
    pm.parent(oneGroup, w = True)
    
    om.MGlobal_displayInfo('circle created: \t%s' % oneHelp.nodeName())   
    return oneGroup,oneHelp

def rootGroup(sel = None):
    if not sel:
        sel = pm.ls(sl = True)
    rootGrps = []
    
    for s in sel:
        
        oneGroup = pm.group(em = True, name = ( s.nodeName() + "_grp" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
        pm.parent(oneGroup, w = True)
        s.setParent(oneGroup)
        
        rootGrps.append(oneGroup)
        
    return(rootGrps)

def insertGroup(sel = None):
    if not sel:
        sel = pm.ls(sl = True)
    
    grpList = []
    for s in sel:
        bakParent = s.getParent()
        oneGroup = pm.group(em = True, name = ( s.nodeName() + "_grp" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
        pm.parent(oneGroup, w = True)
        s.setParent(oneGroup)
        oneGroup.setParent(bakParent)
        grpList.append(oneGroup)
    
    return grpList

def childGroup():
    sel = pm.ls(sl = True)
    for s in sel:
        oneGroup = pm.group(em = True, name = ( s.nodeName() + "_grp" ))
        oneGroup.setParent(s)
        oneGroup.translate.set([0,0,0])
        oneGroup.rotate.set([0,0,0])
        oneGroup.scale.set([1,1,1])
        
def createLoc(rad = 1, sel = pm.ls(sl = True)): 
    locList = []   
    for s in sel:
        tmp = createOneLoc(rad, s)
        locList.append(tmp)
    return locList

def createOneLoc(s, rad = 1, parentToWorld = True):
        s = pm.PyNode(s)
        oneLoc = pm.spaceLocator(a = True, name = (s.name() + "_loc") )
        oneLoc.localScale.set([rad,rad,rad])
        pm.parent(oneLoc, s, r = True)
        if parentToWorld: pm.parent(oneLoc, w = True)
        return oneLoc
    
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



# def to replace old shape with new shape
def createNurbsSphere(rad = 2, oneName = "sphere_ctrl"):
    circ1 = pm.circle(ch = False, o = True, nr = [1,0,0], r = rad, name = oneName)[0]
    circ2 = pm.circle(ch = False, o = True, nr = [0,1,0], r = rad, name = oneName)[0]
    circ3 = pm.circle(ch = False, o = True, nr = [0,0,1], r = rad, name = oneName)[0]
    pm.parent(circ3.getShape(), circ2.getShape(), circ1, s = True, r = True)
    pm.delete(circ3, circ2)
    return circ1

def createCross(d = 1, name = "cross_ctrl"):
    curve = pm.curve( degree = 1, \
    periodic = True, \
    point =[(-2*d, 0, -d), (-d, 0, -d), (-d, 0, -2*d), (d, 0, -2*d), (d,0,-d), (2*d,0,-d), (2*d,0,d), (d,0,d), (d,0,2*d), (-d,0,2*d), (-d,0,d), (-2*d,0,d), (-2*d, 0, -d)], \
    knot = [-2,-1,0,1,2,3,4,5,6,7,8,9,10], \
    name = name)
    
    return curve

def createOneCube(d = 1, name = "cube_ctrl", sel = None):
    curv1 = pm.curve(degree = 1, periodic = True, point = [(-d,d,-d), (-d,d,d), (d,d,d), (d,d,-d),(-d,d,-d) ], knot = [0,1,2,3,4])
    curv2 = pm.curve(degree = 1, periodic = True, point = [(-d,-d,-d), (-d,-d,d), (d,-d,d), (d,-d,-d),(-d,-d,-d) ], knot = [0,1,2,3,4])
    curv3 = pm.curve(degree = 1, periodic = True, point = [(-d,d,-d), (-d,-d,-d), (-d,d,-d)], knot = [0,1,2])
    curv4 = pm.curve(degree = 1, periodic = True, point = [(d,d,-d), (d,-d,-d), (d,d,-d)], knot = [0,1,2])
    curv5 = pm.curve(degree = 1, periodic = True, point = [(-d,d,d), (-d,-d,d), (-d,d,d)], knot = [0,1,2])
    curv6 = pm.curve(degree = 1, periodic = True, point = [(d,d,d), (d,-d,d), (d,d,d)], knot = [0,1,2])
    
    if sel: name = (sel.nodeName() + "_crtl")
    
    curveFinal = pm.group(empty = True, name = name)
    
    pm.parent(curv1.getShape(), curv2.getShape(), curv3.getShape(), curv4.getShape(), curv5.getShape(), curv6.getShape() , curveFinal , shape = True, relative = True)
    
    pm.delete(curv1, curv2, curv3, curv4, curv5, curv6)
    return curveFinal
 