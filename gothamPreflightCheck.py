
#check renderer


def cleanStats():
    maxSubdiv = 8
    #var
    dirs = []
    dirtyFiles=[]
    lambertOnes=[]
    noneMipmapFiles=[]
    goodExts = [".exr", ".hdr"]


    #textures check
    fileList = mc.ls(type = "file")
    for f in fileList:
        
        fPath = mc.getAttr(f+".fileTextureName")
        fileExt = os.path.splitext(fPath)[-1]
        if fileExt not in goodExts:
            dirtyFiles.append(fPath)

        fFilter = mc.getAttr(f+".filterType")
        if fFilter != 1:
            noneMipmapFiles.append(fPath)

    if len(dirtyFiles)>0:
        print "==================================="
        print " bad textures still found in scene."
        print "==================================="
        for p in dirtyFiles:
            print p

    if len(noneMipmapFiles)>0:
        print "==================================="
        print " none mipmap texture filter found."
        print "==================================="
        for f in noneMipmapFiles:
            print f

    #lambert 1 check
    sg = "initialShadingGroup"
    allOutput = mc.listConnections(sg, s=True, sh=True)
    for o in allOutput:
        nodeType = mc.nodeType(o)
        if nodeType == "mesh":
            lambertOnes.append(o)

    if len(lambertOnes)>0:
        print "========================================"
        print " following meshs have Lambert 1 applied."    
        print "========================================"
        for m in lambertOnes:
            print m

    #Vray shader Checks..
    #subdiv check
    vrayMtls = mc.ls(type = "VRayMtl")
    print "----------------------------------------"
    print " checking vray shader settings ..."    
    print "----------------------------------------"
    for mat in vrayMtls:
        rflSub = mc.getAttr(mat+".reflectionSubdivs")
        rfraSub = mc.getAttr(mat+".refractionSubdivs")
        if rflSub > maxSubdiv:
            print mat, "reflection subdiv: ", rflSub

        if rfraSub > maxSubdiv:
            print mat, "refraction subdiv: ", rfraSub


cleanStats()