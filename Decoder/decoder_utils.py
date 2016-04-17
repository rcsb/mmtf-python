
def generateBioAssembly(dataApi, structInflator):
    """ generated source for method generateBioAssembly """
    i = 0
    while i < dataApi.getNumBioassemblies():
        j = 0
        while j < dataApi.getNumTransInBioassembly(i):
            structInflator.setBioAssemblyTrans(i + 1, dataApi.getChainIndexListForTransform(i, j), dataApi.getMatrixForTransform(i, j))
            j += 1
        i += 1

#
# 	 * Generate inter group bonds.
# 	 * Bond indices are specified within the whole structure and start at 0.
# 	 * @param dataApi the interface to the decoded data
# 	 * @param structInflator the interface to put the data into the client object
#
def addInterGroupBonds(dataApi, structInflator):
    """ generated source for method addInterGroupBonds """
    for i in range(len(dataApi.getInterGroupBondOrders)):
        structInflator.setInterGroupBond(dataApi.getInterGroupBondIndices()[i * 2], dataApi.getInterGroupBondIndices()[i * 2 + 1], dataApi.getInterGroupBondOrders()[i])

#
# 	 * Add ancilliary header information to the structure.
# 	 * @param dataApi the interface to the decoded data
# 	 * @param structInflator the interface to put the data into the client object
#
def addHeaderInfo(dataApi, structInflator):
    """ generated source for method addHeaderInfo """
    structInflator.setHeaderInfo(dataApi.getRfree(), dataApi.getRwork(), dataApi.getResolution(), dataApi.getTitle(), dataApi.getDepositionDate(), dataApi.getReleaseDate(), dataApi.getExperimentalMethods())

#
# 	 * Add the crystallographic data to the structure.
# 	 * @param dataApi the interface to the decoded data
# 	 * @param structInflator the interface to put the data into the client object
#
def addXtalographicInfo(dataApi, structInflator):
    """ generated source for method addXtalographicInfo """
    if dataApi.getUnitCell() != None:
        structInflator.setXtalInfo(dataApi.getSpaceGroup(), dataApi.getUnitCell())

#
# 	 * Add the entity info to the structure.
# 	 * @param dataApi the interface to the decoded data
# 	 * @param structInflator the interface to put the data into the client object
#
def addEntityInfo( dataApi, structInflator):
    """ generated source for method addEntityInfo """
    i = 0
    while i < dataApi.getNumEntities():
        chainIdList = []
        counter = 0
        for chainInd in dataApi.getEntityChainIndexList(i):
            chainIdList[counter] = dataApi.getChainIds()[chainInd]
            counter += 1
        structInflator.setEntityInfo(dataApi.getEntityChainIndexList(i), dataApi.getEntitySequence(i), dataApi.getEntityDescription(i), dataApi.getEntityType(i))
        i += 1
