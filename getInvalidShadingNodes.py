
def getInvalidShadingNodes(nodes_to_exclude=['mesh',]):
    """
    Returns a list of invalid shading nodes
    """
    # get a list of all shading groups
    allShadingGroups=mc.ls(type='shadingEngine')
    
    # get a list of currently connected shading groups in the scene
    validShadingGroups=getVRayMeshShadingGroups()
    validShadingGroups.extend(['initialShadingGroup', 'initialParticleSE'])
    validShadingNodes=[]
    
    # add all nodes in history to a list of nodes not NOT delete
    for sg in validShadingGroups:
        hist=mc.listHistory(sg)
        for node in hist:
            if mc.nodeType(node) not in nodes_to_exclude:
                validShadingNodes.append(node)
    
    # subtract connected from all
    invalidShadingGroups=[x for x in allShadingGroups if x not in validShadingGroups]
    """

    #CHECK:all - valid = invalid
    len(allShadingGroups)
    len(validShadingGroups)
    len(invalidShadingGroups)
    
    """    
    # remove invalid shading groups and connected nodes
    nodes_to_delete=[]
    for sg in invalidShadingGroups:
        hist=mc.listHistory(sg)
        for node in hist:
            if node not in validShadingNodes and node not in nodes_to_delete:
                nodes_to_delete.append(node)
        nodes_to_delete.append(sg)
    return list(set(nodes_to_delete))