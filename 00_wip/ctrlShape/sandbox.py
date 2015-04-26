from pprint import pprint
import pymel.core as pm
import maya.mel as mm



import ctrlShape.ctrlShapes as ctrlShapes


curve = pm.ls(sl = 1)[0]
cvsList = (curve.getShape()).getCVs()

for i,cv in enumerate(cvsList):
    tmpCluster = pm.cluster("curve1.cv[%s]" % i)[1]


    
    oneCtrl = ctrlShapes.createNurbsSphere()

