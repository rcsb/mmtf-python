from API.interfaces import DecodedDataInterface
import array_converters
import array_decoders
from Common.Utils import *


class DefaultDecoder(DecodedDataInterface):
    def getRwork(self):
        return self.rWork

    def getNumAtoms(self):
        return len(self.cartnX)

    def getGroupAtomCharges(self, groupInd):
        return self.groupList[groupInd]["atomCharges"]

    def getAtomIds(self):
        return self.atomId

    def getbFactors(self):
        return self.bFactor

    def getNumEntities(self):
        return len(self.entityList)

    def getReleaseDate(self):
        return self.releaseDate

    def getStructureId(self):
        return self.pdbId

    def getResolution(self):
        return self.resolution

    def getSpaceGroup(self):
        return self.spaceGroup

    def getGroupAtomNames(self, groupInd):
        return self.groupList[groupInd]["atomNames"]

    def getMmtfProducer(self):
        return self.mmtfProducer

    def getNumAtomsInGroup(self, groupInd):
        return len(self.groupList[groupInd]["atomNames"])

    def getGroupBondOrders(self, groupInd):
        return self.groupList[groupInd]["bondOrders"]

    def getNumBonds(self):
        pass

    def getGroupsPerChain(self):
        return self.groupsPerChain

    def getGroupSequenceIndices(self):
        return self.seqResGroupList

    def getInsCodes(self):
        return self.insertionCodeList

    def getAltLocIds(self):
        return self.altId

    def getGroupIds(self):
        return self.groupNum

    def getInterGroupBondIndices(self):
        return self.interGroupBondIndices

    def getChainIndexListForTransform(self, bioassemblyIndex, transformationIndex):
        pass
        # return self.bioAssembly[0]

    def getGroupTypeIndices(self):
        pass

    def getxCoords(self):
        pass

    def getNumChains(self):
        pass

    def getNumTransInBioassembly(self, bioassemblyIndex):
        pass

    def getChainIds(self):
        pass

    def getDepositionDate(self):
        pass

    def getTitle(self):
        pass

    def getNumModels(self):
        pass

    def getSecStructList(self):
        pass

    def getGroupChemCompType(self, groupInd):
        return self.groupList[groupInd]["chemComp"]

    def getMmtfVersion(self):
        pass

    def getGroupBondIndices(self, groupInd):
        return self.groupList[groupInd]["bondIndices"]

    def getEntityDescription(self, entityInd):
        pass

    def getChainNames(self):
        pass

    def getExperimentalMethods(self):
        pass

    def getGroupSingleLetterCode(self, groupInd):
        return self.groupList[groupInd]["singleLetterCode"]

    def getEntityChainIndexList(self, entityInd):
        pass

    def getMatrixForTransform(self, bioassemblyIndex, transformationIndex):
        pass

    def getzCoords(self):
        return self.cartnZ

    def getEntityType(self, entityInd):
        pass

    def getGroupName(self, groupInd):
        return self.groupList[groupInd]["groupName"]

    def getRfree(self):
        return self.rFree

    def getChainsPerModel(self):
        return self.chainsPerModel

    def getInterGroupBondOrders(self):
        return self.interGroupBondOrders

    def getEntitySequence(self, entityInd):
        pass

    def getNumBioassemblies(self):
        return len(self.bioAssembly)

    def getNumGroups(self):
        return len(self.groupList)

    def getyCoords(self):
        return self.cartnY

    def getGroupElementNames(self, groupInd):
        return self.groupList[groupInd]["elementNames"]

    def getOccupancies(self):
        self.occupancy

    def getUnitCell(self):
        self.unitCell

    def decode_data(self, inputData):
        self.groupList = array_converters.convert_bytes_to_ints(inputData["groupTypeList"],4)
        # Decode the coordinate  and B-factor arrays.
        self.cartnX = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(inputData["xCoordSmall"],2),array_converters.convert_bytes_to_ints(inputData["xCoordBig"],4))),COORD_DIVIDER )
        self.cartnY = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(inputData["yCoordSmall"],2),array_converters.convert_bytes_to_ints(inputData["yCoordBig"],4))),COORD_DIVIDER )
        self.cartnZ = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(inputData["zCoordSmall"],2),array_converters.convert_bytes_to_ints(inputData["zCoordBig"],4))),COORD_DIVIDER)
        self.bFactor = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(inputData["bFactorSmall"],2),array_converters.convert_bytes_to_ints(inputData["bFactorBig"],4))),OCC_B_FACTOR_DIVIDER)
        # Run length decode the occupancy array
        self.occupancy = array_converters.convert_ints_to_floats(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["occupancyList"],4)),OCC_B_FACTOR_DIVIDER)
        # Run length and delta
        self.atomId = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["atomIdList"],4)))
        # Run length encoded
        self.altId = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["altLocList"],4)))
        self.insertionCodeList = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["insCodeList"],4)))
        # Get the groupNumber
        self.groupNum = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["groupIdList"],4)))
        # Get the group map (all the unique groups in the structure).
        self.groupMap = inputData["groupList"]
        # Get the seqRes groups
        self.seqResGroupList = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(inputData["sequenceIndexList"],4)))
        # Get the number of chains per model
        self.chainsPerModel = inputData["chainsPerModel"]
        self.groupsPerChain = inputData["groupsPerChain"]
        # Get the internal and public facing chain ids
        self.publicChainIds = array_converters.decode_chain_list(inputData["chainNameList"])
        self.chainList = array_converters.decode_chain_list(inputData["chainIdList"])
        self.spaceGroup = inputData["spaceGroup"]
        self.unitCell = inputData["unitCell"]
        self.bioAssembly  = inputData["bioAssemblyList"]
        self.interGroupBondIndices = array_converters.convert_bytes_to_ints(inputData["bondAtomList"],4)
        self.interGroupBondOrders = array_converters.convert_bytes_to_ints(inputData["bondOrderList"],1)
        self.mmtfVersion = inputData["mmtfVersion"]
        self.mmtfProducer = inputData["mmtfProducer"]
        self.entityList = inputData["entityList"]
        self.pdbId = inputData["structureId"]
        # Now get the header data
        self.rFree = inputData["rFree"]
        # Optional fields
        if "rWork" in inputData:
            self.rWork = inputData["rWork"]
        else:
            self.rWork = None
        if "resolution" in inputData:
            self.resolution = inputData["resolution"]
        if "title" in inputData:
            self.title = inputData["title"]
        self.experimentalMethods = inputData["experimentalMethods"]
        # Now get the relase information
        self.depositionDate = inputData["depositionDate"]
        if "releaseDate" in inputData:
            self.releaseDate = inputData["releaseDate"]
        self.secStructInfo = array_converters.convert_bytes_to_ints(inputData["secStructList"],1)
