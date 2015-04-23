from PySide import QtCore
from PySide import QtGui
import pymel.core as pm


def createButton():  
    source = "Button_Object"
    sel = pm.ls(sl = True)
    
    startX = 0
    startY = 0
    
    for s in sel:  
        startX += 15
        
        newName = None
        if s.name().startswith('R') and not s.name().startswith('RF') and not s.name().startswith('RB') :
            newName = 'r' + (s.name()[1:])
        elif s.name().startswith('FR'):
            newName = 'fr' + (s.name()[2:])
        elif s.name().startswith('RF'):
            newName = 'rf' + (s.name()[2:])
        elif s.name().startswith('RB'):
            newName = 'rb' + (s.name()[2:])
        else:
            newName = s.name()
    
        copy = pm.duplicate(source, name = "Button_%s" % newName)
        print(copy)
        pm.setAttr((copy[0]).scaleX, 10)
        pm.setAttr((copy[0]).scaleY, 10)
        pm.setAttr((copy[0]).translateX, startX)
        pm.setAttr((copy[0]).translateY, 10)
        pm.setAttr((copy[0]).multiObjs, s.name())

        
def addIcon(icon = "ButtonIcon_ball_yellow"):
    sel = pm.ls(sl = True)
    
    for s in sel:
    # match name
        newName =  (s.name()).replace('Button', 'ButtonIcon')
        newIcon = pm.duplicate(icon, name = newName)
    
        # connect attributes
    
        try:
            pm.connectAttr('%s.translate' % s,'%s.translate' % newIcon[0] )
        except Exception as ex:
            print ex
            
        try:
            pm.connectAttr('%s.scaleX' % s,'%s.scaleX' % newIcon[0] )
        except Exception as ex:
            print ex
            
        try:
            pm.connectAttr('%s.scaleY' % s,'%s.scaleY' % newIcon[0] )
        except Exception as ex:
            print ex
            


def symetrizeButton():
    root = 'WindowCorner'
    sym = "symetrizer"
    source = pm.ls(sl = True)
    print(source)
    for s in source:
        nameSplit = s.name().split('_')
        
        # rename button
        newName = None
        if nameSplit[1] == 'r':
            nameSplit[1] = 'l'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'fr':
            nameSplit[1] = 'fl'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'rf':
            nameSplit[1] = 'lf'
            gap = '_'
            newName = gap.join(nameSplit)
        elif nameSplit[1] == 'rb':
            nameSplit[1] = 'lb'
            gap = '_'
            newName = gap.join(nameSplit)
        
        # duplicate button
        print(newName)
        copy = pm.duplicate(s, name = newName)
        
        # rename multiobjs
        oldSel = pm.getAttr((copy[0]).multiObjs)
        newSel = oldSel.replace('R_', 'L_')
        pm.setAttr((copy[0]).multiObjs, newSel)
        
        # deparent window corner
        # parent symetrizer
        pm.parent(copy[0], sym)
        
        # invert translateX
        oldX = pm.getAttr(copy[0].translateX)
        pm.setAttr(copy[0].translateX, oldX*-1)
        
        # parent windows corner
        pm.parent(copy[0], root)

symetrizeButton()

def createOffset():
    source = pm.ls(sl = True)
    for s in source:
        oldName = s.name()
        if oldName.endswith('_ctrl'):
            newName = s.name().replace("_ctrl", '_ofst_ctrl')
            print('toto')
            copy = pm.duplicate(s, name = newName)
            tY = pm.getAttr(s.translateY) - 15
            pm.setAttr(copy[0].translateY, tY )
            
            oldSel = pm.getAttr((copy[0]).multiObjs)
            if oldSel.endswith("_ctrl"):
                newSel = oldSel.replace('_ctrl', '_ofst_ctrl')
                pm.setAttr((copy[0]).multiObjs, newSel)

  
def createGrpBut():  
    objCol = ''
    sel = pm.ls(sl = True)
#     buttonGrp = pm.duplicate(sel[-1], name = sel[-1] + '_group' )
    for s in sel:
        if s.hasAttr('multiObjs'):
            print(s.getAttr('multiObjs'))
            objCol = objCol + ' ' + s.getAttr('multiObjs')
    
    print(objCol)
    
    sel = pm.ls(sl = True)
    copyGrp = pm.duplicate(sel[-1], name = (sel[-1].name() + '_grp'))[0]
    
    pm.setAttr(copyGrp.translateY, 10)
    pm.setAttr(copyGrp.translateX, 10)
    pm.setAttr(copyGrp.multiObjs, objCol)


        
createButton()

createGrpBut()

addIcon("ButtonIcon_ball_red")
addIcon("ButtonIcon_ball_blue")
addIcon("ButtonIcon_ball_yellow")
addIcon("ButtonIcon_ball_green")

addIcon("ButtonIcon_cube_red")
addIcon("ButtonIcon_cube_blue")
addIcon("ButtonIcon_cube_blue1")
addIcon("ButtonIcon_cube_yellow")
addIcon("ButtonIcon_cube_green")

addIcon("ButtonIcon_los_blue")
  
createOffset()  