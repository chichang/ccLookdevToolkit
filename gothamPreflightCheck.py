
#check renderer
#quick check file naming
#check ai opaque if in set?
#check if object id is set
#check if there is geo without user id atter
#check if you have OTHER renderer loaded
#check asset parent and transform
import maya.cmds as mc
import re
import os

def validShaderName(assetName, shaderName):

    print "checking shader name: "+ shaderName

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='((?:[a-z][a-z]+))' # Word 2
    re6='(_)'   # Any Single Character 3
    re7='(shad)'    # Word 3
    re8='($)'
    
    rg1 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m1 = rg1.search(shaderName)

    re1='('+assetName+')'   # Word 1
    re2='(_)'   # Any Single Character 1
    re3='.*?'   # Non-greedy match on filler
    re4='(_)'   # Any Single Character 2
    re5='((?:[a-z]+))' # Word 2
    re6='(_)'   # Any Single Character 3
    re7='(shad)'    # Word 3
    re8='($)'

    rg2 = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
    m2 = rg2.search(shaderName)
    
    print m1, m2

    if m1 or m2:
        word1=m2.group(1)
        c1=m2.group(2)
        c2=m2.group(3)
        word2=m2.group(4)
        c3=m2.group(5)
        word3=m2.group(6)
        #print "("+word1+")"+"("+c1+")"+"("+c2+")"+"("+word2+")"+"("+c3+")"+"("+word3+")"+"\n"
        #print "valid shader name:  " + shaderName
        return True
        
    else:
        print "invalid shader name!! :  " + shaderName
        return False




def fomLookdevPreflight():

    """
    Load and Set the Arnold renderer.

    :param xname: 'fom lookdev pre-publish check'
    :param xcategory: 'fom Lookdev'
    """


    #maxSubdiv = 8
    #var
    #dirs=[]

    MIPMAP_FILTER = 1
    badExtFiles=[]
    nonLibTextures=[]
    lambertOnes=[]
    noneMipmapFiles=[]
    allSgUsed=[]
    invaladShaders=[]
    invalidShaderName=[]
    sgNameNotMatch=dict()
    goodExts=[".exr"]
    validShaderTypes=["alSurface"]

    #getting the asset. assuming we are only lookdeving one asset for now.
    rcnulls = mc.ls(type="rigCenterNode")
    if not rcnulls:
        return
    rcnull = rcnulls[0]

    #get meshes that have lambert one assinged
    initialSg = "initialShadingGroup"
    allOutput = mc.listConnections(initialSg, s=True, sh=True)
    for o in allOutput:
        nodeType = mc.nodeType(o)
        if nodeType == "mesh":
            lambertOnes.append(o)

    #textures check
    fileList = mc.ls(type = "file")
    for f in fileList:

        fPath = mc.getAttr(f+".fileTextureName")
        fileExt = os.path.splitext(fPath)[-1]

        #check non lib textures
        if os.getenv("XPUB_LIB") not in fPath:
            nonLibTextures.append(fPath)

        #check texture data type
        if fileExt not in goodExts:
            badExtFiles.append(fPath)

        #check texture filter type
        fFilter = mc.getAttr(f+".filterType")
        if fFilter != MIPMAP_FILTER:
            noneMipmapFiles.append(fPath)


    #checking shaders and shading engine.
    print "using rcnull: ", rcnull
    assetName = mc.getAttr(rcnull+".assetString")
    print "asset name: ", assetName


    assetMeshes = mc.listRelatives(mc.listRelatives(rcnull, f=True, p=True), ad=True, type = "mesh")
    for mesh in assetMeshes:
        connectedSg = mc.listConnections(mesh, type="shadingEngine")[0]
        if connectedSg not in allSgUsed:
            allSgUsed.append(connectedSg)

    #print "getting shader and shading group connections."

    for sg in allSgUsed:
        connectedShader = mc.connectionInfo(sg+".surfaceShader", sfd=True)
        connectedShader = connectedShader.split(".")[0]
        #print sg+ " => " + connectedShader

        #check if shader name is good.
        if not validShaderName(assetName, connectedShader):
            invalidShaderName.append(connectedShader)
        
        #check if shader engine name matches shader name. 
        if sg != connectedShader+"SG":
            sgNameNotMatch[connectedShader] = sg
        
        #check if we are using the shaders we should be using.
        if mc.nodeType(connectedShader) not in validShaderTypes:
            if connectedShader not in invaladShaders:
                invaladShaders.append(connectedShader)


        #check for empty sets

    #filter all errors we found.
    es = ""

    if len(rcnulls) > 1:
        #more than on asset found in the scene.
        es += "========================================\n"
        es += "you have more than one asset in the scene!!\n"
        es += "========================================\n"
        for r in rcnulls:
            es += r + "\n"
        es += "\n"
        es +="checking lookdev for " + rcnulls[0]+"\n"


    if len(lambertOnes) != 0:
        es += "========================================\n"
        es += " following meshs have Lambert 1 applied.\n"    
        es += "========================================\n"
        for m in lambertOnes:
            es += m + "\n"
        es += "\n"

    if len(invaladShaders) != 0:
        es += "========================================\n"
        es += "found invaled shader type used in lookdev!!\n"
        es += "========================================\n"
        for s in invaladShaders:
            es += s + "\n"
        es += "\n"

    if len(invalidShaderName) != 0:
        es += "========================================\n"
        es += "shaders name not good, Please rename!\n"
        es += "========================================\n"
        for s in invalidShaderName:
            es += s + "\n"
        es += "\n"

    if len(sgNameNotMatch.keys()) != 0:
        es += "========================================\n"
        es += "shading Group name not match shader!!\n"
        es += "========================================\n"
        for key in sgNameNotMatch.keys():
            es += key + " => " + sgNameNotMatch[key] + "\n"
        es += "\n"


    if len(badExtFiles) != 0:
        es += "========================================\n"
        es += " bad texture type still found in scene.\n"
        es += "========================================\n"
        for p in badExtFiles:
            es += p + "\n"
        es += "\n"

    if len(noneMipmapFiles) != 0:
        es += "========================================\n"
        es += " none mipmap texture filter found.\n"
        es += "========================================\n"
        for f in noneMipmapFiles:
            es += f + "\n"
        es += "\n"

    if len(nonLibTextures) != 0:
        es += "========================================\n"
        es += " none lib textures found.\n"
        es += "========================================\n"
        for f in nonLibTextures:
            es += f + "\n"
        es += "\n"

    # #Vray shader Checks..
    # #subdiv check
    # vrayMtls = mc.ls(type = "VRayMtl")
    # print "----------------------------------------"
    # print " checking vray shader settings ..."    
    # print "----------------------------------------"
    # for mat in vrayMtls:
    #     rflSub = mc.getAttr(mat+".reflectionSubdivs")
    #     rfraSub = mc.getAttr(mat+".refractionSubdivs")
    #     if rflSub > maxSubdiv:
    #         print mat, "reflection subdiv: ", rflSub

    #     if rfraSub > maxSubdiv:
    #         print mat, "refraction subdiv: ", rfraSub

    #show error
    if es == "":
        es = "lookdev passed pre-publish check."
    mc.confirmDialog( title='Check!', message=es, button=['OK'], defaultButton='OK')