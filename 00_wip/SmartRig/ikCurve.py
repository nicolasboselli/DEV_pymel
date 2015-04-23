#-*- coding: utf-8 -*

import pymel.core as pm
import maya.mel as mm


import pymel.core.nodetypes as nt

'''
Created on 13 dec. 2013

@author: nico
'''

def curveInfo(part = 1):
    sel = pm.ls(sl = True)

    if (len(sel)) == 1:
        for s in sel:
            if pm.nodeType(s.getShape()) == 'nurbsCurve':
                curve = pm.arclen(s, ch = True)
                
                pm.addAttr( s, longName = "part", attributeType = 'double' )
                pm.setAttr( ("%s.part" % s) , keyable = True )
                 
                str =("%s.part = %s.arcLength/%s ;" % (s, curve, part))
                pm.expression(s = str, o = s, ae = True, uc = "all" , n = (s + "_partExp"))
                
            else:
                print 'non conform selection'