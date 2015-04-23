
from pprint import pprint
import pymel.core as pm

# joints = pm.ls(type = 'joint')
# for j in joints:
#     print j.getAttr('radius')
    
# sel = pm.ls(sl = True)[0]
# shpe = sel.getShape()
# print(shpe)
# 
# pprint(pm.listAttr(shpe))
# print shpe.getAttr('spansU')
# print shpe.spansU.get()


# sel = pm.ls(sl = True)[0]
# res = pm.xform(sel, q = True, relative = True, boundingBox = True)
# print res

# get vertex
# get local position vertex
# collect xmax, xmin, ymin, ymax
# calculate dimension
# pm.delete(sel.getShape())
# res = sel.listRelatives(children = True, type = 'transform')
# print res
# print pm.nodeType(sel)

# print sel.shapeName()

pm.parent('ribbon_plane_twist_up', 'ribbon_plane_motion_system')
    
    