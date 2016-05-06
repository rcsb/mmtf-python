#!/usr/bin/env python
from __future__ import print_function
from abc import ABCMeta, abstractmethod

class DecodedDataInterface():
    """An interface describing the data API.

The structural data is accessible through this interface via
a flat structure, instead of the usual hierarchical
data encountered in PDB structures: structure to model to chain to group to atom.
Going back to a hierarchical view of the structure can be achieved by
using the {:link #get_chains_per_model()}, {:link #get_groups_per_chain()} and
{:link #get_group_type_indices()} methods so that the flat arrays can be reconstructed into
a hierarchy.

Please refer to the full MMTF specification available at
<a href="http://mmtf.rcsb.org">http://mmtf.rcsb.org</a>.
Further reference can be found in the <a href="http://mmcif.wwpdb.org/">mmCIF dictionary</a>.

:author Anthony Bradley
:author Jose Duarte"""


    __metaclass__ = ABCMeta



    @abstractmethod
    def get_x_coords(self):
        """Returns an array containing the X coordinates of the atoms in Angstroms.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""

    @abstractmethod
    def get_y_coords(self):
        """Returns an array containing the Y coordinates of the atoms in Angstroms.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""   	
    
    @abstractmethod
    def get_z_coords(self):
        """Returns an array containing the Z coordinates of the atoms in Angstroms.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""


    @abstractmethod
    def get_b_factors(self):
        """Returns an array containing the B-factors (temperature factors) of the atoms in Angstroms^2.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""


    @abstractmethod
    def get_occupancies(self):
        """Returns an array containing the occupancy values of the atoms.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""


    @abstractmethod
    def get_atom_ids(self):
        """Returns an array of atom serial ids (_atom_site.id in mm_c_i_f dictionary).
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""

    @abstractmethod
    def get_alt_loc_ids(self):
        """ Returns an array of alt location ids of the atoms.
    	'\0' specifies a lack of alt id.
    	:return an array of length the number of atoms in the structure, obtainable with {:link #get_num_atoms()}"""

    @abstractmethod
    def get_ins_codes(self):
        """Returns an array containing the insertion codes (pdbx_PDB_ins_code in mm_c_i_f dictionary) for each residue (group).
    	'\0' specifies a lack of insertion code.
    	:return an array with insertion codes, of size {:link #get_num_groups()}
    	:see #get_group_ids()"""

    @abstractmethod
    def get_group_ids(self):
        """Returns an array containing residue numbers (auth_seq_id in mm_c_i_f dictionary) for each residue (group).
    	:return an array with with residue numbers, of size {:link #get_num_groups()}
    	:see #get_ins_codes()"""


    @abstractmethod
    def get_group_name(self, group_ind):
        """Returns the group name for the group specified in {:link #get_group_type_indices()}.
    	to link groups to the 3 letter group name, e.g. HIS.
    	:param group_ind The index of the group specified in {:link #get_group_type_indices()}.
    	:return a 3 letter string specifiying the group name."""

    @abstractmethod
    def get_num_atoms_in_group(self, group_ind):
        """Returns the number of atoms in the group specified in {:link #get_group_type_indices()}.
    	:param group_ind The index of the group specified in {:link #get_group_type_indices()}.
    	:return The number of atoms in the group"""


    @abstractmethod
    def get_group_atom_names(self, group_ind):
        """Returns the atom names (e.g. CB) for the group specified in {:link #get_group_type_indices()}.
    	Atom names are unique for each unique atom in a group.
    	:param group_ind The index of the group specified in {:link #get_group_type_indices()}.
    	:return A list of strings for the atom names."""

    @abstractmethod
    def get_group_element_names(self, group_ind):
        """Returns the IUPAC element names (e.g. Ca is calcium) for the group specified in {:link #get_group_type_indices()}.
    	:param group_ind the index of the group specified in {:link #get_group_type_indices()}.
    	:return an array of strings for the element information."""


    @abstractmethod
    def get_group_bond_orders(self, group_ind):
        """Returns the bond orders for the group specified in {:link #get_group_type_indices()}.
    	A list of integers indicating the bond orders
    	:param group_ind the index of the group specified in {:link #get_group_type_indices()}.
    	:return an array of integers (1,2 or 3) indicating the bond orders."""


    @abstractmethod
    def get_group_bond_indices(self, group_ind):
        """Returns the zero-based bond indices (in pairs) for the group specified in {:link #get_group_type_indices()}.
    	(e.g. 0,1 means there is bond between atom 0 and 1).
    	:param group_ind the index of the group specified in {:link #get_group_type_indices()}.
    	:return an array of integers specifying the bond indices (within the group). Indices are zero indexed."""




    @abstractmethod
    def get_group_atom_charges(self, group_ind):
        """Returns the atom charges for the group specified in {:link #get_group_type_indices()}.
    	:param group_ind the index of the group specified in {:link #get_group_type_indices()}.
    	:return an array of integers indicating the atomic charge for each atom in the group."""

    @abstractmethod
    def get_group_single_letter_code(self, group_ind):
        """Returns the single letter amino acid code or nucleotide code for the
    	group specified in {:link #get_group_type_indices()}.
    	:param group_ind the index of the group specified in {:link #get_group_type_indices()}.
    	:return the single letter amino acid or nucleotide, 'X' if non-standard amino acid or nucleotide"""


    @abstractmethod
    def get_group_chem_comp_type(self, group_ind):
        """Returns the chemical component type for the group specified in {:link #get_group_type_indices()}.
    	:param group_ind The index of the group specified in {:link #get_group_type_indices()}.
    	:return a string (taken from the chemical component dictionary) indicating
    	the type of the group. Corresponds to
    	<a href="http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx.dic/Items/_chem_comp.type.html">http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx.dic/Items/_chem_comp.type.html</a>"""




    @abstractmethod
    def get_group_type_indices(self):
        """Returns an array containing indices to be used to obtain group level information,
    	e.g. through {:link #get_group_atom_charges(int)}.
    	:return an array of length the number of groups (residues) in the structure, obtainable with {:link #get_num_groups()}"""




    @abstractmethod
    def get_group_sequence_indices(self):
        """Returns an array containing the indices of groups (residues) in their corresponding sequences,
    	obtainable through {:link #get_entity_sequence(int)}.
    	The indices are 0-based and specified per entity, -1 indicates the group is not present in the sequence.
    	:return an array of length the number of groups (residues) in the structure, obtainable with {:link #get_num_groups()}"""




    @abstractmethod
    def get_chain_ids(self):
        """Returns an array of internal chain identifiers (asym_ids in mm_c_i_f dictionary), of length the
    	number of chains (polymeric, non-polymeric and water) in the structure.
    	:return an array of length the number of chains in the structure, obtainable with {:link #get_num_chains()}
    	:see #get_chain_names()"""




    @abstractmethod
    def get_chain_names(self):
        """Returns an array of public chain identifiers (auth_ids in mm_c_i_f dictionary), of length the
    	number of chains (polymeric, non-polymeric and water) in the structure.
    	:return an array of length the number of chains in the structure, obtainable with {:link #get_num_chains()}
    	:see #get_chain_ids()"""




    @abstractmethod
    def get_chains_per_model(self):
        """Returns an array containing the number of chains (polymeric/non-polymeric/water) in each model.
    	:return an array of length the number of models in the structure, obtainable with {:link #get_num_models()}"""




    @abstractmethod
    def get_groups_per_chain(self):
        """Returns an array containing the number of groups (residues) in each chain.
    	:return an array of length the number of chains in the structure, obtainable with {:link #get_num_chains()}"""




    @abstractmethod
    def get_space_group(self):
        """Returns the space group of the structure.
    	:return the space group name (e.g. "P 21 21 21") or null if the structure is not crystallographic"""




    @abstractmethod
    def get_unit_cell(self):
        """Returns the 6 floats that describe the unit cell.
    	:return an array of size 6 with the unit cell parameters in order: a, b, c, alpha, beta, gamma"""




    @abstractmethod
    def get_num_bioassemblies(self):
        """Returns the number of bioassemblies in this structure.
    	:return the number of bioassemblies."""




    @abstractmethod
    def get_num_trans_in_bioassembly(self, bioassembly_index):
        """Returns the number of transformations in a given bioassembly.
    	:param bioassembly_index an integer specifying the bioassembly index (zero indexed).
    	:return an integer specifying of transformations in a given bioassembly."""




    @abstractmethod
    def get_chain_index_list_for_transform(self, bioassembly_index, transformation_index):
        """Returns the list of chain indices for the given transformation for the given bioassembly.
    	:param bioassembly_index an integer specifying the bioassembly index (zero indexed).
    	:param transformation_index an integer specifying the  index (zero indexed) for the desired transformation.
    	:return a list of indices showing the chains involved in this transformation."""




    @abstractmethod
    def get_matrix_for_transform(self, bioassembly_index, transformation_index):
        """Returns a 4x4 transformation matrix for the given transformation for the given bioassembly.
    	It is row-packed as per the convention of vecmath. (The first four elements are in the first row of the
    	overall matrix).
    	:param bioassembly_index an integer specifying the bioassembly index (zero indexed).
    	:param transformation_index an integer specifying the  index for the desired transformation (zero indexed).
    	:return the transformation matrix for this transformation."""




    @abstractmethod
    def get_inter_group_bond_indices(self):
        """Returns the zero-based bond indices (in pairs) for the structure.
    	(e.g. 0,1 means there is bond between atom 0 and 1).
    	:return an array of integers specifying the bond indices (within the structure). Indices are zero-based."""




    @abstractmethod
    def get_inter_group_bond_orders(self):
        """Returns an array of bond orders (1,2,3) of inter-group bonds with length <em>number of inter-group bonds</em>
    	:return the bond orders for bonds within a group"""




    @abstractmethod
    def get_mmtf_version(self):
        """Returns the MMTF version number (from the specification).
    	:return the version"""




    @abstractmethod
    def get_mmtf_producer(self):
        """Returns a string describing the producer of the MMTF file.
    	e.g. "RCSB-PDB Generator---version: 6b8635f8d319beea9cd7cc7f5dd2649578ac01a0"
    	:return a string describing the producer"""




    @abstractmethod
    def get_num_entities(self):
        """Returns the number of entities (as defined in mmCIF dictionary) in the structure
    	:return the number of entities in the structure"""


    @abstractmethod
    def get_entity_description(self, entity_ind):
        """Returns the entity description (as defined in mmCIF dictionary)
        for the entity specified by the index.
        :param entity_ind the index of the specified entity.
        :return the description of the entity
    """




    @abstractmethod
    def get_entity_type(self, entity_ind):
        """Returns the entity type (polymer, non-polymer, water) for the entity specified by the index.
    	:param entity_ind the index of the specified entity.
    	:return the entity type (polymer, non-polymer, water)"""




    @abstractmethod
    def get_entity_chain_index_list(self, entity_ind):
        """Returns the chain indices for the entity specified by the index.
    	:param entity_ind the index of the specified entity.
    	:return the chain index list - referencing the entity to the chains."""



    @abstractmethod
    def get_entity_sequence(self, entity_ind):
        """Returns the sequence for the entity specified by the index.
    	:param entity_ind the index of the specified entity.
    	:return the one letter sequence for this entity. Empty string if no sequence is applicable.
    """




    @abstractmethod
    def get_structure_id(self):
        """Returns the identifier of the structure.
    	For instance the 4-letter PDB id
    	:return the identifier"""




    @abstractmethod
    def get_num_models(self):
        """Returns the number of models in the structure.
    	:return the number of models"""




    @abstractmethod
    def get_num_bonds(self):
        """Returns the total number of bonds in the structure
    	:return the number of bonds"""




    @abstractmethod
    def get_num_chains(self):
        """Returns the number of chains (for all models) in the structure.
    	:return the number of chains for all models
    	:see #get_chains_per_model()"""




    @abstractmethod
    def get_num_groups(self):
        """Returns the number of groups (residues) in the structure that have
    	experimentally determined 3D coordinates.
    	:return the number of residues in the structure, for all models and chains"""




    @abstractmethod
    def get_num_atoms(self):
        """Returns the number of atoms in the structure.
    	:return the number of atoms in the structure, for all models and chains"""




    @abstractmethod
    def get_rfree(self):
        """Returns the Rfree of the dataset.
    	:return the Rfree value"""




    @abstractmethod
    def get_rwork(self):
        """Returns the Rwork of the dataset.
    	:return the Rwork value"""




    @abstractmethod
    def get_resolution(self):
        """Returns the resolution of the dataset.
    	:return the resolution value in Angstroms"""




    @abstractmethod
    def get_title(self):
        """Returns the title of the structure.
    	:return the title of the structure."""




    @abstractmethod
    def get_experimental_methods(self):
        """Returns the experimental methods as an array of strings. Normally only one
        experimental method is available, but structures solved with hybrid methods will
        have more than one method.
        The possible experimental method values are described in
        <a href="http://mmcif.wwpdb.org/dictionaries/mmcif_pdbx_v40.dic/Items/_exptl.method.html">data item <em>_exptl.method</em> of the mm_c_i_f dictionary</a>
        :return the list of experimental methods"""




    @abstractmethod
    def get_deposition_date(self):
        """Returns the deposition date of the structure as a string
    	in ISO time standard format. https://www.cl.cam.ac.uk/~mgk25/iso-time.html
    	:return the deposition date of the structure."""




    @abstractmethod
    def get_release_date(self):
        """Returns the release date of the structure as a string
    	in ISO time standard format. https://www.cl.cam.ac.uk/~mgk25/iso-time.html
    	:return the release date of the structure. """



    @abstractmethod
    def get_sec_struct_list(self):
        """The secondary structure information for the structure as a list of integers
    	:return the array of secondary structure informations
    	"""

class DataTransferInterface(object):
    """Abstract class that can be implemented to inflate a given MMTF data source."""
    __metaclass__ = ABCMeta



    @abstractmethod
    def init_structure(self, total_num_bonds, total_num_atoms, total_num_groups, total_num_chains, total_num_models, structure_id):
        """Used before any additions to do any required pre-processing.
    	For example the user could use this to specify the amount of memory to be allocated.
    	:param total_num_bonds the total number of bonds in the structure
    	:param total_num_atoms the total number of atoms found in the data.
    	:param total_num_groups the total number of groups found in the data.
    	:param total_num_chains the total number of chains found in the data.
    	:param total_num_models the total number of models found in the data.
    	:param structure_id an identifier for the structure (e.g. PDB id)."""


    @abstractmethod
    def finalize_structure(self):
        """A generic function to be used at the end of all data addition to do required cleanup on the structure"""




    @abstractmethod
    def set_model_info(self, model_id, chain_count):
        """Sets the number of chains for a given model.
    	:param model_id identifier of the model within the structure
    	:param chain_count total number of chains within this model"""




    @abstractmethod
    def set_chain_info(self, chain_id, chain_name, group_count):
        """Sets the information for a given chain.
    	:param chain_id chain identifier - length of one to four
    	:param chain_name chain name - public chain id
    	:param group_count number of groups/residues in chain"""




    @abstractmethod
    def set_entity_info(self, chain_indices, sequence, description, type_):
        """Sets the entity level annotation for a chain(s). ChainIds is a list of integers that indicate the chains this information
    	refers to. Sequence is the one letter amino acid sequence. Description and title are both free forms strings describing the entity and
    	acting as a title for the entity.
    	:param chain_indices the indices of the chain this refers to.
    	:param sequence the full sequence of the entity
    	:param description the text description of the entity
    	:param type as a string (POLYMER/NON-POLYMER and WATER)"""




    @abstractmethod
    def set_group_info(self, group_name, group_number, insertion_code, group_type, atom_count, bond_count, single_letter_code, sequence_index, secondary_structure_type):
        """Sets the information for a given group / residue with atomic data.
    	:param group_name 3 letter code name of this group/residue
    	:param group_number sequence position of this group
    	:param insertion_code the one letter insertion code
    	:param group_type a string indicating the type of group (as found in the chemcomp dictionary. Empty string if none available.
    	:param atom_count the number of atoms in the group
    	:param bond_count the number of unique bonds in the group
    	:param single_letter_code the single letter code of the group
    	:param sequence_index the index of this group in the sequence
    	:param secondary_structure_type the type of secondary structure used (types are according to DSSP and number to
    	type mappings are defined in the specification)"""




    @abstractmethod
    def set_atom_info(self, atom_name, serial_number, alternative_location_id, x, y, z, occupancy, temperature_factor, element, charge):
        """Sets the atom level information for a given atom.
    	:param atom_name 1-3 long string of the unique name of the atom
    	:param serial_number a number counting atoms in a structure
    	:param alternative_location_id a character indicating the alternate
    	location of the atom
    	:param x the x cartesian coordinate
    	:param y the y cartesian coordinate
    	:param z the z cartesian coordinate
    	:param occupancy the atomic occupancy
    	:param temperature_factor the B factor (temperature factor)
    	:param element a 1-3 long string indicating the chemical element of the atom
    	:param charge the atomic charge"""




    @abstractmethod
    def set_bio_assembly_trans(self, bio_assembly_index, input_chain_indices, input_transform):
        """Sets a single Bioassembly transformation to a structure. bio_assembly_id indicates the index of the bioassembly.
    	:param bio_assembly_index An integer index of this bioassembly.
    	:param input_chain_indices The integer indices of the chains involved in this bioassembly.
    	:param input_transform A list of doubles indicating the transform for this bioassembly."""




    @abstractmethod
    def set_xtal_info(self, space_group, unit_cell):
        """Sets the space group and unit cell information.
    	:param space_group the space group name, e.g. "P 21 21 21"
    	:param unit_cell an array of length 6 with the unit cell parameters in order: a, b, c, alpha, beta, gamma"""




    @abstractmethod
    def set_group_bond(self, atom_index_one, atom_index_two, bond_order):
        """Sets an intra-group bond.
    	:param atom_index_one the atom index of the first partner in the bond
    	:param atom_index_two the atom index of the second partner in the bond
    	:param bond_order the bond order """




    @abstractmethod
    def set_inter_group_bond(self, atom_index_one, atom_index_two, bond_order):
        """Sets an inter-group bond.
    	:param atom_index_one the atom index of the first partner in the bond
    	:param atom_index_two the atom index of the second partner in the bond
    	:param bond_order the bond order"""




    @abstractmethod
    def set_header_info(self, r_free, r_work, resolution, title, deposition_date, release_date, experimnetal_methods):
        """Sets the header information.
    	:param r_free the measured R-Free for the structure
    	:param r_work the measure R-Work for the structure
    	:param resolution the resolution of the structure
    	:param title the title of the structure
    	:param deposition_date the deposition date of the structure
    	:param release_date the release date of the structure
    	:param experimnetal_methods the list of experimental methods in the structure"""

