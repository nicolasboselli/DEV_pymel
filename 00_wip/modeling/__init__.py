import pymel.core as pm
from pprint import pprint
from pymel.core.datatypes import *


def averageVertex():
    
    vert = pm.ls(sl = True)
    
    if len(vert)>0:
        for v in vert:
            print v
    #         print v.getTranslation()
            conVert =  v.connectedVertices()
            x = 0
            y = 0
            z = 0
            
            
            for c in conVert:
                pos = c.getPosition()
                print(pos[0])
                x = x + pos[0]
                y = y + pos[1]
                z = z + pos[2]
                
            sum = [x/len(conVert),y//len(conVert),z//len(conVert)]
            print(sum)
            
            v.setPosition(sum)
                
            v.setColor(Color.red )

            
vertTmp = pm.ls(sl = True)
# pprint(vert)
vert = []
for elt in vertTmp:
    if not len(elt)>1:
        vert.append(elt)
    else:
        for v in elt:
            vert.append(v)
            
for v in vert:
    print(v.getPosition())
    oldPos = v.getPosition()
    newPos = [0, oldPos[1], oldPos[2]]
    v.setPosition(newPos)
# if len(vert)>0:
#     for v in vert:
#         oldPos = v.getPosition()
#         print(oldPos)