
import maya.cmds as mc
def deleteMAttrs():
    attrsToDelete = [ "mShape", "mSubd", "mMaterial" ]
    #delete on all meshes
    allMesh = mc.ls(type="mesh")
    for mesh in allMesh:
        attrs = mc.listAttr(mesh)
        for attr in attrsToDelete:
            if attr in attrs:
                toDelete = mesh+"."+attr 
                #check for locked attr
                if mc.getAttr(toDelete, l=True):
                    mc.setAttr(toDelete, l=False)
                #delete attr
                print "deleting:  ", toDelete
                mc.deleteAttr(toDelete)