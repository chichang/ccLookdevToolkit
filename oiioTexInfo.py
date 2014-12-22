
#===============================================================
#
#  print out texture info by calling oiiotool in maya.
#
#===============================================================

#imports
import maya.cmds as mc
import subprocess
import os

def printTexInfo():

    #udim tags (Vray and Arnold)
    udimTags = ["<udim>", "<UDIM>"]

    #subprocess call list
    callList = ["oiiotool", "--info", "-v"]
    
    #get selected file node
    try:
        fileNode = mc.ls(sl=True, type="file")[0]
        print "getting path for: " + fileNode
    except:
        mc.warning("select a file node please.")
        return

    #get file path
    filePath = mc.getAttr(fileNode+".fileTextureName")
    print "file path is: ", filePath

    #get one texture if udim found
    for tag in udimTags:

        if tag in filePath:
            #find one of the textures
            for i in range (1001, 1099):
                checkPath = filePath.replace(tag, str(i))
                #print checkPath
                if os.path.exists(checkPath):
                    print "found texture: " + checkPath
                    filePath = checkPath
                    break
        else:
            pass

    if os.path.exists(filePath):
        #get info
        print "getting texture info..."

        #call oiio
        callList.append(filePath)
        print "calling: ", callList

        try:
            p = subprocess.Popen(callList, stdout=subprocess.PIPE)
            out, err = p.communicate()
            
            message = "====================================================\n"
            message += "Texture info for : " + fileNode + "\n"
            message += "Texture checked: " + filePath + "\n"
            message += "====================================================\n\n"
            message += out
            
        except:
            message = "Error calling oiiotool."

        #display result
        mc.confirmDialog( title='Texture Info: ' + fileNode, message=message, button=['OK'], defaultButton='OK')

    else:
        mc.warning("could not find any texture. does texture exist ?")
        return

