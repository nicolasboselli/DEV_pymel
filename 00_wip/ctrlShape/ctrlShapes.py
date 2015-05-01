'''
Created on 31 janv. 2015

@author: nico
'''

# execute ctrl mel:(one proc by ctrl? import all proc and call one? insert mel in python function? load mel in dcitionnary? load mel path in dictionnary)
# replace ctrl mel created on Selection

from pprint import pprint
import pymel.core as pm
import maya.mel as mm
import os
from glob import glob


# def to replace old shape with new shape
def createNurbsSphere(rad = 2, oneName = "sphere_ctrl"):
    circ1 = pm.circle(ch = False, o = True, nr = [1,0,0], r = rad, name = oneName)[0]
    circ2 = pm.circle(ch = False, o = True, nr = [0,1,0], r = rad, name = oneName)[0]
    circ3 = pm.circle(ch = False, o = True, nr = [0,0,1], r = rad, name = oneName)[0]
    pm.parent(circ3.getShape(), circ2.getShape(), circ1, s = True, r = True)
    pm.delete(circ3, circ2)
    return circ1

def createCross(d = 1, name = "cross_ctrl" ):
    curve = pm.curve( degree = 1, \
    periodic = True, \
    point =[(-2*d, 0, -d), (-d, 0, -d), (-d, 0, -2*d), (d, 0, -2*d), (d,0,-d), (2*d,0,-d), (2*d,0,d), (d,0,d), (d,0,2*d), (-d,0,2*d), (-d,0,d), (-2*d,0,d), (-2*d, 0, -d)], \
    knot = [-2,-1,0,1,2,3,4,5,6,7,8,9,10], \
    name = name)
    return curve

def createOneCube(d = 1, name = "cube_ctrl"):
    curv1 = pm.curve(degree = 1, periodic = True, point = [(-d,d,-d), (-d,d,d), (d,d,d), (d,d,-d),(-d,d,-d) ], knot = [0,1,2,3,4])
    curv2 = pm.curve(degree = 1, periodic = True, point = [(-d,-d,-d), (-d,-d,d), (d,-d,d), (d,-d,-d),(-d,-d,-d) ], knot = [0,1,2,3,4])
    curv3 = pm.curve(degree = 1, periodic = True, point = [(-d,d,-d), (-d,-d,-d), (-d,d,-d)], knot = [0,1,2])
    curv4 = pm.curve(degree = 1, periodic = True, point = [(d,d,-d), (d,-d,-d), (d,d,-d)], knot = [0,1,2])
    curv5 = pm.curve(degree = 1, periodic = True, point = [(-d,d,d), (-d,-d,d), (-d,d,d)], knot = [0,1,2])
    curv6 = pm.curve(degree = 1, periodic = True, point = [(d,d,d), (d,-d,d), (d,d,d)], knot = [0,1,2])
    
    curveFinal = pm.group(empty = True, name = name)
    
    pm.parent(curv1.getShape(), curv2.getShape(), curv3.getShape(), curv4.getShape(), curv5.getShape(), curv6.getShape() , curveFinal , shape = True, relative = True)
    
    pm.delete(curv1, curv2, curv3, curv4, curv5, curv6)
    return curveFinal



