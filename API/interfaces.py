#!/usr/bin/env python
""" generated source for module DecodedDataInterface """
from __future__ import print_function
from abc import ABCMeta, abstractmethod
# package: org.rcsb.mmtf.api
# 
#  * An interface describing the data API.
#  * 
#  * <p>
#  * The structural data is accessible through this interface via 
#  * a flat structure, instead of the usual hierarchical 
#  * data encountered in PDB structures: structure to model to chain to group to atom.
#  * Going back to a hierarchical view of the structure can be achieved by 
#  * using the {@link #getChainsPerModel()}, {@link #getGroupsPerChain()} and 
#  * {@link #getGroupTypeIndices()} methods so that the flat arrays can be reconstructed into
#  * a hierarchy.   
#  * 
#  * <p>
#  * Please refer to the full MMTF specification available at 
#  * <a href="http://mmtf.rcsb.org">http://mmtf.rcsb.org</a>.
#  * Further reference can be found in the <a href="http://mmcif.wwpdb.org/">mmCIF dictionary</a>.
#  * 
#  * @author Anthony Bradley
#  * @author Jose Duarte
#  
class DecodedDataInterface():
    """ generated source for interface DecodedDataInterface """
    __metaclass__ = ABCMeta
    # 
    # 	 * Returns an array containing the X coordinates of the atoms in Angstroms.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getxCoords(self):
        """ generated source for method getxCoords """

    # 
    # 	 * Returns an array containing the Y coordinates of the atoms in Angstroms.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getyCoords(self):
        """ generated source for method getyCoords """

    # 
    # 	 * Returns an array containing the Z coordinates of the atoms in Angstroms.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getzCoords(self):
        """ generated source for method getzCoords """

    # 
    # 	 * Returns an array containing the B-factors (temperature factors) of the atoms in Angstroms^2.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getbFactors(self):
        """ generated source for method getbFactors """

    # 
    # 	 * Returns an array containing the occupancy values of the atoms.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getOccupancies(self):
        """ generated source for method getOccupancies """

    # 
    # 	 * Returns an array of atom serial ids (_atom_site.id in mmCIF dictionary).
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()}
    # 	 
    @abstractmethod
    def getAtomIds(self):
        """ generated source for method getAtomIds """

    # 
    # 	 * Returns an array of location ids of the atoms.
    # 	 * '\0' specifies a lack of alt id.
    # 	 * @return an array of length the number of atoms in the structure, obtainable with {@link #getNumAtoms()} 
    # 	 
    @abstractmethod
    def getAltLocIds(self):
        """ generated source for method getAltLocIds """

    # 
    # 	 * Returns an array containing the insertion codes (pdbx_PDB_ins_code in mmCIF dictionary) for each residue (group). 
    # 	 * '\0' specifies a lack of insertion code.
    # 	 * @return an array with insertion codes, of size {@link #getNumGroups()}
    # 	 * @see #getGroupIds()
    # 	 
    @abstractmethod
    def getInsCodes(self):
        """ generated source for method getInsCodes """

    # 
    # 	 * Returns an array containing residue numbers (auth_seq_id in mmCIF dictionary) for each residue (group).
    # 	 * @return an array with with residue numbers, of size {@link #getNumGroups()} 
    # 	 * @see #getInsCodes()
    # 	 
    @abstractmethod
    def getGroupIds(self):
        """ generated source for method getGroupIds """

    # 
    # 	 * Returns the group name for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * to link groups to the 3 letter group name, e.g. HIS.
    # 	 * @param groupInd The index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return a 3 letter string specifiying the group name.
    # 	 
    @abstractmethod
    def getGroupName(self, groupInd):
        """ generated source for method getGroupName """

    # 
    # 	 * Returns the number of atoms in the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @param groupInd The index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return The number of atoms in the group
    # 	 
    @abstractmethod
    def getNumAtomsInGroup(self, groupInd):
        """ generated source for method getNumAtomsInGroup """

    #  
    # 	 * Returns the atom names (e.g. CB) for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * Atom names are unique for each unique atom in a group.
    # 	 * @param groupInd The index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return A list of strings for the atom names. 
    # 	 * 
    @abstractmethod
    def getGroupAtomNames(self, groupInd):
        """ generated source for method getGroupAtomNames """

    #  
    # 	 * Returns the IUPAC element names (e.g. Ca is calcium) for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @param groupInd the index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return an array of strings for the element information. 
    # 	 * 
    @abstractmethod
    def getGroupElementNames(self, groupInd):
        """ generated source for method getGroupElementNames """

    #  
    # 	 * Returns the bond orders for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * A list of integers indicating the bond orders
    # 	 * @param groupInd the index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return an array of integers (1,2 or 3) indicating the bond orders. 
    # 	 * 
    @abstractmethod
    def getGroupBondOrders(self, groupInd):
        """ generated source for method getGroupBondOrders """

    #  
    # 	 * Returns the zero-based bond indices (in pairs) for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * (e.g. 0,1 means there is bond between atom 0 and 1).
    # 	 * @param groupInd the index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return an array of integers specifying the bond indices (within the group). Indices are zero indexed.
    # 	 * 
    @abstractmethod
    def getGroupBondIndices(self, groupInd):
        """ generated source for method getGroupBondIndices """

    #  
    # 	 * Returns the atom charges for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @param groupInd the index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return an array of integers indicating the atomic charge for each atom in the group.
    # 	 
    @abstractmethod
    def getGroupAtomCharges(self, groupInd):
        """ generated source for method getGroupAtomCharges """

    #  
    # 	 * Returns the single letter amino acid code or nucleotide code for the 
    # 	 * group specified in {@link #getGroupTypeIndices()}.
    # 	 * @param groupInd the index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return the single letter amino acid or nucleotide, 'X' if non-standard amino acid or nucleotide
    # 	 
    @abstractmethod
    def getGroupSingleLetterCode(self, groupInd):
        """ generated source for method getGroupSingleLetterCode """

    #  
    # 	 * Returns the chemical component type for the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @param groupInd The index of the group specified in {@link #getGroupTypeIndices()}.
    # 	 * @return a string (taken from the chemical component dictionary) indicating 
    # 	 * the type of the group. Corresponds to 
    # 	 * <a href="http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx.dic/Items/_chem_comp.type.html">http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx.dic/Items/_chem_comp.type.html</a>
    # 	 
    @abstractmethod
    def getGroupChemCompType(self, groupInd):
        """ generated source for method getGroupChemCompType """

    # 
    # 	 * Returns an array containing indices to be used to obtain group level information, 
    # 	 * e.g. through {@link #getGroupAtomCharges(int)}.
    # 	 * @return an array of length the number of groups (residues) in the structure, obtainable with {@link #getNumGroups()}
    # 	 
    @abstractmethod
    def getGroupTypeIndices(self):
        """ generated source for method getGroupTypeIndices """

    # 
    # 	 * Returns an array containing the indices of groups (residues) in their corresponding sequences,
    # 	 * obtainable through {@link #getEntitySequence(int)}.
    # 	 * The indices are 0-based and specified per entity, -1 indicates the group is not present in the sequence.
    # 	 * @return an array of length the number of groups (residues) in the structure, obtainable with {@link #getNumGroups()}
    # 	 
    @abstractmethod
    def getGroupSequenceIndices(self):
        """ generated source for method getGroupSequenceIndices """

    # 
    # 	 * Returns an array of internal chain identifiers (asym_ids in mmCIF dictionary), of length the 
    # 	 * number of chains (polymeric, non-polymeric and water) in the structure. 
    # 	 * @return an array of length the number of chains in the structure, obtainable with {@link #getNumChains()}
    # 	 * @see #getChainNames()
    # 	 
    @abstractmethod
    def getChainIds(self):
        """ generated source for method getChainIds """

    # 
    # 	 * Returns an array of public chain identifiers (auth_ids in mmCIF dictionary), of length the 
    # 	 * number of chains (polymeric, non-polymeric and water) in the structure. 
    # 	 * @return an array of length the number of chains in the structure, obtainable with {@link #getNumChains()}
    # 	 * @see #getChainIds()
    # 	 
    @abstractmethod
    def getChainNames(self):
        """ generated source for method getChainNames """

    # 
    # 	 * Returns an array containing the number of chains (polymeric/non-polymeric/water) in each model.
    # 	 * @return an array of length the number of models in the structure, obtainable with {@link #getNumModels()}
    # 	 
    @abstractmethod
    def getChainsPerModel(self):
        """ generated source for method getChainsPerModel """

    # 
    # 	 * Returns an array containing the number of groups (residues) in each chain.
    # 	 * @return an array of length the number of chains in the structure, obtainable with {@link #getNumChains()}
    # 	 
    @abstractmethod
    def getGroupsPerChain(self):
        """ generated source for method getGroupsPerChain """

    # 
    # 	 * Returns the space group of the structure.
    # 	 *
    # 	 * @return the space group name (e.g. "P 21 21 21") or null if the structure is not crystallographic
    # 	 
    @abstractmethod
    def getSpaceGroup(self):
        """ generated source for method getSpaceGroup """

    # 
    # 	 * Returns the 6 floats that describe the unit cell.
    # 	 * @return an array of size 6 with the unit cell parameters in order: a, b, c, alpha, beta, gamma
    # 	 
    @abstractmethod
    def getUnitCell(self):
        """ generated source for method getUnitCell """

    # 
    # 	 * Returns the number of bioassemblies in this structure.
    # 	 * @return the number of bioassemblies.
    # 	 
    @abstractmethod
    def getNumBioassemblies(self):
        """ generated source for method getNumBioassemblies """

    # 
    # 	 * Returns the number of transformations in a given bioassembly.
    # 	 * @param bioassemblyIndex an integer specifying the bioassembly index (zero indexed).
    # 	 * @return an integer specifying of transformations in a given bioassembly.
    # 	 
    @abstractmethod
    def getNumTransInBioassembly(self, bioassemblyIndex):
        """ generated source for method getNumTransInBioassembly """

    # 
    # 	 * Returns the list of chain indices for the given transformation for the given bioassembly.
    # 	 * @param bioassemblyIndex an integer specifying the bioassembly index (zero indexed).
    # 	 * @param transformationIndex an integer specifying the  index (zero indexed) for the desired transformation.
    # 	 * @return a list of indices showing the chains involved in this transformation.
    # 	 
    @abstractmethod
    def getChainIndexListForTransform(self, bioassemblyIndex, transformationIndex):
        """ generated source for method getChainIndexListForTransform """

    # 
    # 	 * Returns a 4x4 transformation matrix for the given transformation for the given bioassembly.
    # 	 * It is row-packed as per the convention of vecmath. (The first four elements are in the first row of the
    # 	 * overall matrix).
    # 	 * @param bioassemblyIndex an integer specifying the bioassembly index (zero indexed).
    # 	 * @param transformationIndex an integer specifying the  index for the desired transformation (zero indexed).
    # 	 * @return the transformation matrix for this transformation.
    # 	 
    @abstractmethod
    def getMatrixForTransform(self, bioassemblyIndex, transformationIndex):
        """ generated source for method getMatrixForTransform """

    # 
    # 	 * Returns the zero-based bond indices (in pairs) for the structure.
    # 	 * (e.g. 0,1 means there is bond between atom 0 and 1).
    # 	 * @return an array of integers specifying the bond indices (within the structure). Indices are zero-based.
    # 	 
    @abstractmethod
    def getInterGroupBondIndices(self):
        """ generated source for method getInterGroupBondIndices """

    # 
    # 	 * Returns an array of bond orders (1,2,3) of inter-group bonds with length <em>number of inter-group bonds</em>
    # 	 * @return the bond orders for bonds within a group
    # 	 
    @abstractmethod
    def getInterGroupBondOrders(self):
        """ generated source for method getInterGroupBondOrders """

    # 
    # 	 * Returns the MMTF version number (from the specification).
    # 	 * @return the version
    # 	 
    @abstractmethod
    def getMmtfVersion(self):
        """ generated source for method getMmtfVersion """

    # 
    # 	 * Returns a string describing the producer of the MMTF file.
    # 	 * e.g. "RCSB-PDB Generator---version: 6b8635f8d319beea9cd7cc7f5dd2649578ac01a0"
    # 	 * @return a string describing the producer
    # 	 
    @abstractmethod
    def getMmtfProducer(self):
        """ generated source for method getMmtfProducer """

    # 
    # 	 * Returns the number of entities (as defined in mmCIF dictionary) in the structure
    # 	 * @return the number of entities in the structure 
    # 	 
    @abstractmethod
    def getNumEntities(self):
        """ generated source for method getNumEntities """

    # 
    # 	 * Returns the entity description (as defined in mmCIF dictionary) 
    # 	 * for the entity specified by the index.
    # 	 * @param entityInd the index of the specified entity.
    # 	 * @return the description of the entity
    # 	 
    @abstractmethod
    def getEntityDescription(self, entityInd):
        """ generated source for method getEntityDescription """

    # 
    # 	 * Returns the entity type (polymer, non-polymer, water) for the entity specified by the index.
    # 	 * @param entityInd the index of the specified entity.
    # 	 * @return the entity type (polymer, non-polymer, water)
    # 	 
    @abstractmethod
    def getEntityType(self, entityInd):
        """ generated source for method getEntityType """

    # 
    # 	 * Returns the chain indices for the entity specified by the index.
    # 	 * @param entityInd the index of the specified entity.
    # 	 * @return the chain index list - referencing the entity to the chains.
    # 	 
    @abstractmethod
    def getEntityChainIndexList(self, entityInd):
        """ generated source for method getEntityChainIndexList """

    # 
    # 	 * Returns the sequence for the entity specified by the index.
    # 	 * @param entityInd the index of the specified entity.
    # 	 * @return the one letter sequence for this entity. Empty string if no sequence is applicable.
    # 	 
    @abstractmethod
    def getEntitySequence(self, entityInd):
        """ generated source for method getEntitySequence """

    # 
    # 	 * Returns the identifier of the structure.
    # 	 * For instance the 4-letter PDB id
    # 	 * @return the identifier
    # 	 
    @abstractmethod
    def getStructureId(self):
        """ generated source for method getStructureId """

    # 
    # 	 * Returns the number of models in the structure.
    # 	 * @return the number of models
    # 	 
    @abstractmethod
    def getNumModels(self):
        """ generated source for method getNumModels """

    # 
    # 	 * Returns the total number of bonds in the structure
    # 	 * @return the number of bonds
    # 	 
    @abstractmethod
    def getNumBonds(self):
        """ generated source for method getNumBonds """

    # 
    # 	 * Returns the number of chains (for all models) in the structure.
    # 	 * @return the number of chains for all models
    # 	 * @see #getChainsPerModel()
    # 	 
    @abstractmethod
    def getNumChains(self):
        """ generated source for method getNumChains """

    # 
    # 	 * Returns the number of groups (residues) in the structure that have
    # 	 * experimentally determined 3D coordinates.
    # 	 * @return the number of residues in the structure, for all models and chains
    # 	 
    @abstractmethod
    def getNumGroups(self):
        """ generated source for method getNumGroups """

    # 
    # 	 * Returns the number of atoms in the structure.
    # 	 * @return the number of atoms in the structure, for all models and chains
    # 	 
    @abstractmethod
    def getNumAtoms(self):
        """ generated source for method getNumAtoms """

    # 
    # 	 * Returns the Rfree of the dataset.
    # 	 * @return the Rfree value
    # 	 
    @abstractmethod
    def getRfree(self):
        """ generated source for method getRfree """

    # 
    # 	 * Returns the Rwork of the dataset.
    # 	 * @return the Rwork value
    # 	 
    @abstractmethod
    def getRwork(self):
        """ generated source for method getRwork """

    # 
    # 	 * Returns the resolution of the dataset.
    # 	 * @return the resolution value in Angstroms
    # 	 
    @abstractmethod
    def getResolution(self):
        """ generated source for method getResolution """

    # 
    # 	 * Returns the title of the structure.
    # 	 * @return the title of the structure.
    # 	 
    @abstractmethod
    def getTitle(self):
        """ generated source for method getTitle """

    # 
    # 	 * Returns the experimental methods as an array of strings. Normally only one 
    # 	 * experimental method is available, but structures solved with hybrid methods will
    # 	 * have more than one method. 
    # 	 * The possible experimental method values are described in 
    # 	 * <a href="http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v40.dic/Items/_exptl.method.html">data item <em>_exptl.method</em> of the mmCIF dictionary</a>
    # 	 * @return the list of experimental methods 
    # 	 
    @abstractmethod
    def getExperimentalMethods(self):
        """ generated source for method getExperimentalMethods """

    # 
    # 	 * Returns the deposition date of the structure as a string
    # 	 * in ISO time standard format. https://www.cl.cam.ac.uk/~mgk25/iso-time.html
    # 	 * @return the deposition date of the structure.
    # 	 
    @abstractmethod
    def getDepositionDate(self):
        """ generated source for method getDepositionDate """

    # 
    # 	 * Returns the release date of the structure as a string
    # 	 * in ISO time standard format. https://www.cl.cam.ac.uk/~mgk25/iso-time.html
    # 	 * @return the release date of the structure.
    # 	 
    @abstractmethod
    def getReleaseDate(self):
        """ generated source for method getReleaseDate """

    # 
    # 	 * The secondary structure information for the structure as a list of integers
    # 	 * @return the array of secondary structure informations
    # 	 
    @abstractmethod
    def getSecStructList(self):
        """ generated source for method getSecStructList """

class DataTransferInterface(object):
    """ generated source for interface DataTransferInterface """
    __metaclass__ = ABCMeta
    #
    # 	 * Used before any additions to do any required pre-processing.
    # 	 * For example the user could use this to specify the amount of memory to be allocated.
    # 	 * @param totalNumBonds the total number of bonds in the structure
    # 	 * @param totalNumAtoms the total number of atoms found in the data.
    # 	 * @param totalNumGroups the total number of groups found in the data.
    # 	 * @param totalNumChains the total number of chains found in the data.
    # 	 * @param totalNumModels the total number of models found in the data.
    # 	 * @param structureId an identifier for the structure (e.g. PDB id).
    #
    @abstractmethod
    def initStructure(self, totalNumBonds, totalNumAtoms, totalNumGroups, totalNumChains, totalNumModels, structureId):
        """ generated source for method initStructure """

    #
    # 	 * A generic function to be used at the end of all data addition to do required cleanup on the structure
    #
    @abstractmethod
    def finalizeStructure(self):
        """ generated source for method finalizeStructure """

    #
    # 	 * Sets the number of chains for a given model.
    # 	 * @param modelId identifier of the model within the structure
    # 	 * @param chainCount total number of chains within this model
    #
    @abstractmethod
    def setModelInfo(self, modelId, chainCount):
        """ generated source for method setModelInfo """

    #
    # 	 * Sets the information for a given chain.
    # 	 * @param chainId chain identifier - length of one to four
    # 	 * @param chainName chain name - public chain id
    # 	 * @param groupCount number of groups/residues in chain
    #
    @abstractmethod
    def setChainInfo(self, chainId, chainName, groupCount):
        """ generated source for method setChainInfo """

    #
    # 	 * Sets the entity level annotation for a chain(s). ChainIds is a list of integers that indicate the chains this information
    # 	 * refers to. Sequence is the one letter amino acid sequence. Description and title are both free forms strings describing the entity and
    # 	 * acting as a title for the entity.
    # 	 * @param chainIndices the indices of the chain this refers to.
    # 	 * @param sequence the full sequence of the entity
    # 	 * @param description the text description of the entity
    # 	 * @param type as a string (POLYMER/NON-POLYMER and WATER)
    #
    @abstractmethod
    def setEntityInfo(self, chainIndices, sequence, description, type_):
        """ generated source for method setEntityInfo """

    #
    # 	 * Sets the information for a given group / residue with atomic data.
    # 	 * @param groupName 3 letter code name of this group/residue
    # 	 * @param groupNumber sequence position of this group
    # 	 * @param insertionCode the one letter insertion code
    # 	 * @param groupType a string indicating the type of group (as found in the chemcomp dictionary. Empty string if none available.
    # 	 * @param atomCount the number of atoms in the group
    # 	 * @param bondCount the number of unique bonds in the group
    # 	 * @param singleLetterCode the single letter code of the group
    # 	 * @param sequenceIndex the index of this group in the sequence
    # 	 * @param secondaryStructureType the type of secondary structure used (types are according to DSSP and number to
    # 	 * type mappings are defined in the specification)
    #
    @abstractmethod
    def setGroupInfo(self, groupName, groupNumber, insertionCode, groupType, atomCount, bondCount, singleLetterCode, sequenceIndex, secondaryStructureType):
        """ generated source for method setGroupInfo """

    #
    # 	 * Sets the atom level information for a given atom.
    # 	 * @param atomName 1-3 long string of the unique name of the atom
    # 	 * @param serialNumber a number counting atoms in a structure
    # 	 * @param alternativeLocationId a character indicating the alternate
    # 	 * location of the atom
    # 	 * @param x the x cartesian coordinate
    # 	 * @param y the y cartesian coordinate
    # 	 * @param z the z cartesian coordinate
    # 	 * @param occupancy the atomic occupancy
    # 	 * @param temperatureFactor the B factor (temperature factor)
    # 	 * @param element a 1-3 long string indicating the chemical element of the atom
    # 	 * @param charge the atomic charge
    #
    @abstractmethod
    def setAtomInfo(self, atomName, serialNumber, alternativeLocationId, x, y, z, occupancy, temperatureFactor, element, charge):
        """ generated source for method setAtomInfo """

    #
    # 	 * Sets a single Bioassembly transformation to a structure. bioAssemblyId indicates the index of the bioassembly.
    # 	 * @param bioAssemblyIndex An integer index of this bioassembly.
    # 	 * @param inputChainIndices The integer indices of the chains involved in this bioassembly.
    # 	 * @param inputTransform A list of doubles indicating the transform for this bioassembly.
    #
    @abstractmethod
    def setBioAssemblyTrans(self, bioAssemblyIndex, inputChainIndices, inputTransform):
        """ generated source for method setBioAssemblyTrans """

    #
    # 	 * Sets the space group and unit cell information.
    # 	 *
    # 	 * @param spaceGroup the space group name, e.g. "P 21 21 21"
    # 	 * @param unitCell an array of length 6 with the unit cell parameters in order: a, b, c, alpha, beta, gamma
    #
    @abstractmethod
    def setXtalInfo(self, spaceGroup, unitCell):
        """ generated source for method setXtalInfo """

    #
    # 	 * Sets an intra-group bond.
    # 	 *
    # 	 * @param atomIndexOne the atom index of the first partner in the bond
    # 	 * @param atomIndexTwo the atom index of the second partner in the bond
    # 	 * @param bondOrder the bond order
    #
    @abstractmethod
    def setGroupBond(self, atomIndexOne, atomIndexTwo, bondOrder):
        """ generated source for method setGroupBond """

    #
    # 	 * Sets an inter-group bond.
    # 	 * @param atomIndexOne the atom index of the first partner in the bond
    # 	 * @param atomIndexTwo the atom index of the second partner in the bond
    # 	 * @param bondOrder the bond order
    #
    @abstractmethod
    def setInterGroupBond(self, atomIndexOne, atomIndexTwo, bondOrder):
        """ generated source for method setInterGroupBond """

    #
    # 	 * Sets the header information.
    # 	 * @param rFree the measured R-Free for the structure
    # 	 * @param rWork the measure R-Work for the structure
    # 	 * @param resolution the resolution of the structure
    # 	 * @param title the title of the structure
    # 	 * @param depositionDate the deposition date of the structure
    # 	 * @param releaseDate the release date of the structure
    # 	 * @param experimnetalMethods the list of experimental methods in the structure
    #
    @abstractmethod
    def setHeaderInfo(self, rFree, rWork, resolution, title, depositionDate, releaseDate, experimnetalMethods):
        """ generated source for method setHeaderInfo """

