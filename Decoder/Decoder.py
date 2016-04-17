from IPython.core.tests.test_inputtransformer import transform_and_reset

from API.interfaces import DecodedDataInterface,DataTransferInterface
import array_converters
import array_decoders
from Common.Utils import *
import decoder_utils


def add_atom_data(self, data_setters, atom_names, element_names, atom_charges, atom_counter, group_atom_ind):

    atom_name = atom_names[group_atom_ind]
    element = element_names[group_atom_ind]
    charge = atom_charges[group_atom_ind]
    alternative_location_id = self.get_alt_loc_ids()[self.atom_counter]
    serial_number = self.get_atom_ids()[self.atom_counter]
    x = self.get_x_coords()[self.atom_counter]
    z = self.get_z_coords()[self.atom_counter]
    y = self.get_y_coords()[self.atom_counter]
    occupancy = self.get_occupancies()[self.atom_counter]
    temperature_factor = self.get_b_factors()[self.atom_counter]
    data_setters.set_atom_info(atom_name, serial_number, alternative_location_id, x, y, z, occupancy, temperature_factor, element, charge)


def add_group_bonds(data_setters, bond_indices, bond_orders):
    for bond_index in range(len(bond_orders)):
        data_setters.set_group_bond(bond_indices[bond_index*2],bond_indices[bond_index*2+1],bond_orders[bond_index])


def add_group(self, data_setters, group_ind):

    group_type_ind = self.get_group_type_indices()[group_ind]

    atom_count = self.get_num_atoms_in_group(group_type_ind)

    current_group_number = self.get_group_ids()[group_ind]
    #
    insertion_code = self.get_ins_codes()[group_ind]
    data_setters.set_group_info(self.get_group_name(group_type_ind), current_group_number, insertion_code, self.get_group_chem_comp_type(group_type_ind), atom_count, self.get_num_bonds(), self.get_group_single_letter_code(group_type_ind), self.get_group_sequence_indices()[group_ind], self.get_sec_struct_list()[group_ind])
    for group_atom_ind in range(atom_count):
        add_atom_data(self, data_setters, self.get_group_atom_names(group_type_ind), self.get_group_element_names(group_type_ind), self.get_group_atom_charges(group_type_ind), self.atom_counter, group_atom_ind)
        self.atom_counter +=1
    add_group_bonds(data_setters, self.get_group_bond_indices(group_type_ind), self.get_group_bond_orders(group_type_ind))
    return atom_count


def add_chain_info(self, data_setters, chain_index):
    chain_id = self.get_chain_ids()[chain_index]
    chain_name = self.get_chain_names()[chain_index]
    num_groups = self.get_groups_per_chain()[chain_index]
    data_setters.set_chain_info(chain_id, chain_name, num_groups)
    next_ind = self.group_counter + num_groups
    last_ind = self.group_counter
    for group_ind in range(last_ind, next_ind):
        add_group(self, data_setters, group_ind)
        self.group_counter +=1


    self.chain_counter+=1


def add_atomic_information(self, data_setters):
    for model_chains in self.get_chains_per_model():
        data_setters.set_model_info(self.model_counter, model_chains)
        tot_chains_this_model = self.chain_counter + model_chains
        last_chain_counter = self.chain_counter
        for chain_index in range(last_chain_counter,tot_chains_this_model):
            add_chain_info(self, data_setters, chain_index)
        self.model_counter+=1



class DefaultDecoder(DecodedDataInterface):

    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0


    """The default decoder class"""
    def get_rwork(self):
        return self.r_work

    def get_num_atoms(self):
        return len(self.cartnX)

    def get_group_atom_charges(self, group_ind):
        return self.group_list[group_ind]["atom_charges"]

    def get_atom_ids(self):
        return self.atom_id

    def get_b_factors(self):
        return self.b_factor

    def get_num_entities(self):
        return len(self.entity_list)

    def get_release_date(self):
        return self.release_date

    def get_structure_id(self):
        return self.pdb_id

    def get_resolution(self):
        return self.resolution

    def get_space_group(self):
        return self.space_group

    def get_group_atom_names(self, group_ind):
        return self.group_map[group_ind]["atom_names"]

    def get_mmtf_producer(self):
        return self.mmtf_producer

    def get_num_atoms_in_group(self, group_ind):
        return len(self.group_map[group_ind]["atom_names"])

    def get_group_bond_orders(self, group_ind):
        return self.group_map[group_ind]["bond_orders"]

    def get_num_bonds(self):
        num_bonds = len(self.inter_group_bond_orders)
        for in_int in self.group_list:
            num_bonds += len(self.group_map[in_int]["bond_orders"])
        return num_bonds

    def get_groups_per_chain(self):
        return self.groups_per_chain

    def get_group_sequence_indices(self):
        return self.seq_res_group_list

    def get_ins_codes(self):
        return self.insertion_code_list

    def get_alt_loc_ids(self):
        return self.alt_id

    def get_group_ids(self):
        return self.group_num

    def get_inter_group_bond_indices(self):
        return self.inter_group_bond_indices

    def get_group_type_indices(self):
        return self.group_list

    def get_x_coords(self):
        return self.cartnX

    def get_num_chains(self):
        sum = 0
        for x in self.chains_per_model:
            sum+=x
        return x

    def get_chain_ids(self):
        return self.chain_list

    def get_deposition_date(self):
        return self.deposition_date

    def get_title(self):
        return self.title

    def get_num_models(self):
        return len(self.chains_per_model)

    def get_sec_struct_list(self):
        return self.sec_struct_info

    def get_group_chem_comp_type(self, group_ind):
        return self.group_map[group_ind]["chem_comp"]

    def get_mmtf_version(self):
        return self.mmtf_version

    def get_group_bond_indices(self, group_ind):
        return self.group_map[group_ind]["bondIndices"]

    def get_chain_names(self):
        return self.public_chain_ids

    def get_experimental_methods(self):
        return self.experimental_methods

    def get_group_single_letter_code(self, group_ind):
        return self.group_map[group_ind]["singleLetterCode"]

    def get_z_coords(self):
        return self.cartnZ


    def get_group_name(self, group_ind):
        return self.group_map[group_ind]["groupName"]

    def get_rfree(self):
        return self.r_free

    def get_chains_per_model(self):
        return self.chains_per_model

    def get_inter_group_bond_orders(self):
        return self.inter_group_bond_orders

    def get_num_bioassemblies(self):
        return len(self.bio_assembly)

    def get_num_groups(self):
        return len(self.group_list)

    def get_y_coords(self):
        return self.cartnY

    def get_group_element_names(self, group_ind):
        return self.group_map[group_ind]["elementNames"]

    def get_occupancies(self):
        self.occupancy

    def get_unit_cell(self):
        self.unit_cell

    def get_chain_index_list_for_transform(self, bioassembly_index, transformation_index):
        return self.bio_assembly[bioassembly_index][transformation_index]["chainIndexList"]

    def get_matrix_for_transform(self, bioassembly_index, transformation_index):
        return self.bio_assembly[bioassembly_index][transformation_index]["matrix"]

    def get_num_trans_in_bioassembly(self, bioassembly_index):
        return len(self.bio_assembly[bioassembly_index])

    def get_entity_description(self, entity_ind):
        return self.entity_list[entity_ind]["description"]

    def get_entity_chain_index_list(self, entity_ind):
        return self.entity_list[entity_ind]["chainIndexList"]

    def get_entity_type(self, entity_ind):
        return self.entity_list[entity_ind]["type"]

    def get_entity_sequence(self, entity_ind):
        return self.entity_list[entity_ind]["sequence"]

    def decode_data(self, input_data):
        self.group_list = array_converters.convert_bytes_to_ints(input_data["groupTypeList"],4)
        # Decode the coordinate  and B-factor arrays.
        self.cartnX = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(input_data["xCoordSmall"],2),array_converters.convert_bytes_to_ints(input_data["xCoordBig"],4))),COORD_DIVIDER )
        self.cartnY = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(input_data["yCoordSmall"],2),array_converters.convert_bytes_to_ints(input_data["yCoordBig"],4))),COORD_DIVIDER )
        self.cartnZ = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(input_data["zCoordSmall"],2),array_converters.convert_bytes_to_ints(input_data["zCoordBig"],4))),COORD_DIVIDER)
        self.b_factor = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(input_data["bFactorSmall"],2),array_converters.convert_bytes_to_ints(input_data["bFactorBig"],4))),OCC_B_FACTOR_DIVIDER)
        # Run length decode the occupancy array
        self.occupancy = array_converters.convert_ints_to_floats(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["occupancyList"],4)),OCC_B_FACTOR_DIVIDER)
        # Run length and delta
        self.atom_id = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["atomIdList"],4)))
        # Run length encoded
        self.alt_id = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["altLocList"],4)))
        self.insertion_code_list = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["insCodeList"],4)))
        # Get the group_number
        self.group_num = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["groupIdList"],4)))
        # Get the group map (all the unique groups in the structure).
        self.group_map = input_data["groupList"]
        # Get the seq_res groups
        self.seq_res_group_list = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["sequenceIndexList"],4)))
        # Get the number of chains per model
        self.chains_per_model = input_data["chainsPerModel"]
        self.groups_per_chain = input_data["groupsPerChain"]
        # Get the internal and public facing chain ids
        self.public_chain_ids = array_converters.decode_chain_list(input_data["chainNameList"])
        self.chain_list = array_converters.decode_chain_list(input_data["chainIdList"])
        self.space_group = input_data["spaceGroup"]
        self.unit_cell = input_data["unitCell"]
        self.bio_assembly  = input_data["bioAssemblyList"]
        self.inter_group_bond_indices = array_converters.convert_bytes_to_ints(input_data["bondAtomList"],4)
        self.inter_group_bond_orders = array_converters.convert_bytes_to_ints(input_data["bondOrderList"],1)
        self.mmtf_version = input_data["mmtfVersion"]
        self.mmtf_producer = input_data["mmtfProducer"]
        self.entity_list = input_data["entityList"]
        self.pdb_id = input_data["structureId"]
        # Now get the header data
        self.r_free = input_data["rFree"]
        # Optional fields
        if "rWork" in input_data:
            self.r_work = input_data["rWork"]
        else:
            self.r_work = None
        if "resolution" in input_data:
            self.resolution = input_data["resolution"]
        if "title" in input_data:
            self.title = input_data["title"]
        self.experimental_methods = input_data["experimentalMethods"]
        # Now get the relase information
        self.deposition_date = input_data["depositionDate"]
        if "releaseDate" in input_data:
            self.release_date = input_data["releaseDate"]
        self.sec_struct_info = array_converters.convert_bytes_to_ints(input_data["secStructList"],1)

    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters
        :type data_setters: DataTransferInterface
        """
        # First initialise the structure
        data_setters.init_structure(self.get_num_bonds(), self.get_num_atoms(), self.get_num_groups(),
                                   self.get_num_chains(), self.get_num_models(), self.get_structure_id())

        # First add the atomic data
        add_atomic_information(self,data_setters)
        # Set the header info
        decoder_utils.add_header_info(self, data_setters)
        # Set the xtalographic info
        decoder_utils.add_xtalographic_info(self, data_setters)
        # Set the bioassembly info
        decoder_utils.generate_bio_assembly(self, data_setters)
        # Set the intergroup bonds
        decoder_utils.add_inter_group_bonds(self, data_setters)
        # Set the entity information
        decoder_utils.add_entity_info(self, data_setters)
        # Finally call the finalize function
        data_setters.finalize_structure()