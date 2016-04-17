from IPython.core.tests.test_inputtransformer import transform_and_reset

from API.interfaces import DecodedDataInterface,DataTransferInterface
import array_converters
import array_decoders
from Common.Utils import *
import decoder_utils


def addAtomData(self, data_setters, atom_names, element_names, atom_charges, atom_counter, group_atom_ind):

    atomName = atom_names[group_atom_ind]
    element = element_names[group_atom_ind]
    charge = atom_charges[group_atom_ind]
    alternativeLocationId = self.getAltLocIds()[self.atom_counter]
    serialNumber = self.getAtomIds()[self.atom_counter]
    x = self.getxCoords()[self.atom_counter]
    z = self.getzCoords()[self.atom_counter]
    y = self.getyCoords()[self.atom_counter]
    occupancy = self.getOccupancies()[self.atom_counter]
    temperatureFactor = self.getbFactors()[self.atom_counter]
    data_setters.setAtomInfo(atomName, serialNumber, alternativeLocationId, x, y, z, occupancy, temperatureFactor, element, charge)


def addGroupBonds(data_setters, bond_indices, bond_orders):
    for bond_index in range(len(bond_orders)):
        data_setters.setGroupBond(bond_indices[bond_index*2],bond_indices[bond_index*2+1],bond_orders[bond_index])


def add_group(self, data_setters, group_ind):

    group_type_ind = self.getGroupTypeIndices()[group_ind]

    atomCount = self.getNumAtomsInGroup(group_type_ind)

    currentGroupNumber = self.getGroupIds()[group_ind]
    #
    insertionCode = self.getInsCodes()[group_ind]
    data_setters.setGroupInfo(self.getGroupName(group_type_ind), currentGroupNumber, insertionCode, self.getGroupChemCompType(group_type_ind), atomCount, self.getNumBonds(), self.getGroupSingleLetterCode(group_type_ind), self.getGroupSequenceIndices()[group_ind], self.getSecStructList()[group_ind])
    for group_atom_ind in range(atomCount):
        addAtomData(self, data_setters, self.getGroupAtomNames(group_type_ind), self.getGroupElementNames(group_type_ind), self.getGroupAtomCharges(group_type_ind), self.atom_counter, group_atom_ind)
        self.atom_counter +=1
    addGroupBonds(data_setters, self.getGroupBondIndices(group_type_ind), self.getGroupBondOrders(group_type_ind))
    return atomCount

def addOrUpdateChainInfo(self, data_setters, chain_index):
    chain_id = self.getChainIds()[chain_index]
    chain_name = self.getChainNames()[chain_index]
    num_groups = self.getGroupsPerChain()[chain_index]
    data_setters.setChainInfo(chain_id, chain_name, num_groups)
    next_ind = self.group_counter + num_groups
    last_ind = self.group_counter
    for group_ind in range(last_ind, next_ind):
        add_group(self, data_setters, group_ind)
        self.group_counter +=1


    self.chain_counter+=1


def addAtomicInformation(self, data_setters):
    for model_chains in self.getChainsPerModel():
        data_setters.setModelInfo(self.model_counter, model_chains)
        totChainsThisModel = self.chain_counter + model_chains
        lastChainCounter = self.chainCounter
        for chain_index in range(lastChainCounter,totChainsThisModel):
            addOrUpdateChainInfo(self, data_setters, chain_index)
        self.model_counter+=1



class DefaultDecoder(DecodedDataInterface):

    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0


    """The default decoder class"""
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
        return self.groupMap[groupInd]["atomNames"]

    def getMmtfProducer(self):
        return self.mmtfProducer

    def getNumAtomsInGroup(self, groupInd):
        return len(self.groupMap[groupInd]["atomNames"])

    def getGroupBondOrders(self, groupInd):
        return self.groupMap[groupInd]["bondOrders"]

    def getNumBonds(self):
        num_bonds = len(self.interGroupBondOrders)
        for in_int in self.groupList:
            num_bonds += len(self.groupMap[in_int]["bondOrders"])
        return num_bonds

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

    def getGroupTypeIndices(self):
        return self.groupList

    def getxCoords(self):
        return self.cartnX

    def getNumChains(self):
        sum = 0
        for x in self.chainsPerModel:
            sum+=x
        return x

    def getChainIds(self):
        return self.chainList

    def getDepositionDate(self):
        return self.depositionDate

    def getTitle(self):
        return self.title

    def getNumModels(self):
        return len(self.chainsPerModel)

    def getSecStructList(self):
        return self.secStructInfo

    def getGroupChemCompType(self, groupInd):
        return self.groupMap[groupInd]["chemComp"]

    def getMmtfVersion(self):
        return self.mmtfVersion

    def getGroupBondIndices(self, groupInd):
        return self.groupMap[groupInd]["bondIndices"]

    def getChainNames(self):
        return self.publicChainIds

    def getExperimentalMethods(self):
        return self.experimentalMethods

    def getGroupSingleLetterCode(self, groupInd):
        return self.groupMap[groupInd]["singleLetterCode"]

    def getzCoords(self):
        return self.cartnZ


    def getGroupName(self, groupInd):
        return self.groupMap[groupInd]["groupName"]

    def getRfree(self):
        return self.rFree

    def getChainsPerModel(self):
        return self.chainsPerModel

    def getInterGroupBondOrders(self):
        return self.interGroupBondOrders

    def getNumBioassemblies(self):
        return len(self.bioAssembly)

    def getNumGroups(self):
        return len(self.groupList)

    def getyCoords(self):
        return self.cartnY

    def getGroupElementNames(self, groupInd):
        return self.groupMap[groupInd]["elementNames"]

    def getOccupancies(self):
        self.occupancy

    def getUnitCell(self):
        self.unitCell

    def getChainIndexListForTransform(self, bioassemblyIndex, transformationIndex):
        return self.bioAssembly[bioassemblyIndex][transformationIndex]["chainIndexList"]

    def getMatrixForTransform(self, bioassemblyIndex, transformationIndex):
        return self.bioAssembly[bioassemblyIndex][transformationIndex]["matrix"]

    def getNumTransInBioassembly(self, bioassemblyIndex):
        return len(self.bioAssembly[bioassemblyIndex])

    def getEntityDescription(self, entityInd):
        return self.entityList[entityInd]["description"]

    def getEntityChainIndexList(self, entityInd):
        return self.entityList[entityInd]["chainIndexList"]

    def getEntityType(self, entityInd):
        return self.entityList[entityInd]["type"]

    def getEntitySequence(self, entityInd):
        return self.entityList[entityInd]["sequence"]

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

    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters
        :type data_setters: DataTransferInterface
        """
        # First initialise the structure
        data_setters.initStructure(self.getNumBonds(), self.getNumAtoms(), self.getNumGroups(),
                                   self.getNumChains(), self.getNumModels(), self.getStructureId())

        # First add the atomic data
        addAtomicInformation(self,data_setters)
        # Set the header info
        decoder_utils.addHeaderInfo(self, data_setters)
        # Set the xtalographic info
        decoder_utils.addXtalographicInfo(self, data_setters)
        # Set the bioassembly info
        decoder_utils.generateBioAssembly(self, data_setters)
        # Set the intergroup bonds
        decoder_utils.addInterGroupBonds(self, data_setters)
        # Set the entity information
        decoder_utils.addEntityInfo(self, data_setters)
        # Finally call the finalize function
        data_setters.finalizeStructure()