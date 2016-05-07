import decoder_utils
from MMTF.Common.Utils import  *
from MMTF.API.interfaces import DecodedDataInterface
import array_converters
import array_decoders


class MMTFDecoder(DecodedDataInterface):
    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0
    def get_rwork(self):
        return self.r_work

    def get_num_atoms(self):
        return len(self.cartnX)

    def get_group_atom_charges(self, group_ind):
        return self.group_map[group_ind]["atomChargeList"]

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
        return self.group_map[group_ind]["atomNameList"]

    def get_mmtf_producer(self):
        return self.mmtf_producer

    def get_num_atoms_in_group(self, group_ind):
        return len(self.group_map[group_ind]["atomNameList"])

    def get_group_bond_orders(self, group_ind):
        return self.group_map[group_ind]["bondOrderList"]

    def get_num_bonds(self):
        num_bonds = len(self.inter_group_bond_orders)
        for in_int in self.group_list:
            num_bonds += len(self.group_map[in_int]["bondOrderList"])
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
        return self.group_map[group_ind]["chemCompType"]

    def get_mmtf_version(self):
        return self.mmtf_version

    def get_group_bond_indices(self, group_ind):
        return self.group_map[group_ind]["bondAtomList"]

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
        return self.group_map[group_ind]["elementList"]

    def get_occupancies(self):
        return self.occupancy

    def get_unit_cell(self):
        return self.unit_cell

    def get_chain_index_list_for_transform(self, bioassembly_index, transformation_index):
        return self.bio_assembly[bioassembly_index]["transformList"][transformation_index]["chainIndexList"]

    def get_matrix_for_transform(self, bioassembly_index, transformation_index):
        return self.bio_assembly[bioassembly_index]["transformList"][transformation_index]["matrix"]

    def get_num_trans_in_bioassembly(self, bioassembly_index):
        return len(self.bio_assembly[bioassembly_index]["transformList"])

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
        # Run length decode the occupancy array
        if "bFactorSmall" in input_data and "bFactorBig" in input_data:
            self.b_factor = array_converters.convert_ints_to_floats(array_decoders.delta_decode(array_converters.combine_integers(array_converters.convert_bytes_to_ints(input_data["bFactorSmall"],2),array_converters.convert_bytes_to_ints(input_data["bFactorBig"],4))),OCC_B_FACTOR_DIVIDER)
        else:
            self.b_factor = []
        if "occupancyList" in input_data:
            self.occupancy = array_converters.convert_ints_to_floats(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["occupancyList"],4)),OCC_B_FACTOR_DIVIDER)
        else:
            self.occupancy = []
        # Run length and delta
        if "atomIdList" in input_data:
            self.atom_id = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["atomIdList"],4)))
        else:
            self.atom_id = []
        # Run length encoded
        if "altLocList" in input_data:
            self.alt_id = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["altLocList"],4)))
        else:
            self.alt_id = []
        if "insCodeList" in input_data:
            self.insertion_code_list = array_converters.convert_ints_to_chars(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["insCodeList"],4)))
        else:
            self.insertion_code_list = []
        # Get the group_number
        self.group_num = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["groupIdList"],4)))
        # Get the group map (all the unique groups in the structure).
        self.group_map = input_data["groupList"]
        # Get the seq_res groups
        if "sequenceIndexList" in input_data:
            self.seq_res_group_list = array_decoders.delta_decode(array_decoders.run_length_decode(array_converters.convert_bytes_to_ints(input_data["sequenceIndexList"],4)))
        else:
            self.seq_res_group_list = []
        # Get the number of chains per model
        self.chains_per_model = input_data["chainsPerModel"]
        self.groups_per_chain = input_data["groupsPerChain"]
        # Get the internal and public facing chain ids
        if "chainNameList" in input_data:
            self.public_chain_ids = array_converters.decode_chain_list(input_data["chainNameList"])
        else:
            self.public_chain_ids = []
        self.chain_list = array_converters.decode_chain_list(input_data["chainIdList"])
        self.space_group = input_data["spaceGroup"]
        self.inter_group_bond_indices = array_converters.convert_bytes_to_ints(input_data["bondAtomList"],4)
        self.inter_group_bond_orders = array_converters.convert_bytes_to_ints(input_data["bondOrderList"],1)
        self.mmtf_version = input_data["mmtfVersion"]
        self.mmtf_producer = input_data["mmtfProducer"]
        self.pdb_id = input_data["structureId"]
        # Now get the header data
        # Optional fields
        if "entityList" in input_data:
            self.entity_list = input_data["entityList"]
        else:
            self.entity_list = []
        if "bioAssemblyList" in input_data:
            self.bio_assembly = input_data["bioAssemblyList"]
        else:
            self.bio_assembly = []
        if "rFree" in input_data:
            self.r_free = input_data["rFree"]
        else:
            self.r_free = None
        if "rWork" in input_data:
            self.r_work = input_data["rWork"]
        else:
            self.r_work = None
        if "resolution" in input_data:
            self.resolution = input_data["resolution"]
        if "title" in input_data:
            self.title = input_data["title"]
        if "experimentalMethods" in input_data:
            self.experimental_methods = input_data["experimentalMethods"]
        else:
            self.experimental_methods = None
        # Now get the relase information
        if "depositionData" in input_data:
            self.deposition_date = input_data["depositionDate"]
        else:
            self.deposition_date = None
        if "releaseDate" in input_data:
            self.release_date = input_data["releaseDate"]
        else:
            self.release_date = None
        if "unitCell" in input_data:
            self.unit_cell = input_data["unitCell"]
        else:
            self.unit_cell = None

        self.sec_struct_info = array_converters.convert_bytes_to_ints(input_data["secStructList"],1)

    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters
        :type data_setters: DataTransferInterface
        """
        # First initialise the structure
        num_bonds = len(self.inter_group_bond_orders)
        for in_int in self.group_list:
            num_bonds += len(self.group_map[in_int]["bondOrderList"])
        data_setters.init_structure(num_bonds, len(self.cartnX), len(self.group_list),
                                   len(self.chain_list), len(self.chains_per_model), self.get_structure_id())

        # Set the entity information
        decoder_utils.add_entity_info(self, data_setters)
        # First add the atomic data
        decoder_utils.add_atomic_information(self,data_setters)
        # Set the header info
        decoder_utils.add_header_info(self, data_setters)
        # Set the xtalographic info
        decoder_utils.add_xtalographic_info(self, data_setters)
        # Set the bioassembly info
        decoder_utils.generate_bio_assembly(self, data_setters)
        # Set the intergroup bonds
        decoder_utils.add_inter_group_bonds(self, data_setters)

        # Finally call the finalize function
        data_setters.finalize_structure()