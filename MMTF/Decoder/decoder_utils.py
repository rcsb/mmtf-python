
def add_atom_data(self, data_setters, atom_names, element_names, atom_charges, atom_counter, group_atom_ind):
    """Add the atomic data to the DataTransferInterface.
    :param """
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

def generate_bio_assembly(data_api, struct_inflator):
    """Generate the bioassembly data.
    :param data_api the interface to the decoded data
    :param struct_inflator the interface to put the data into the client object"""
    i = 0
    while i < data_api.get_num_bioassemblies():
        j = 0
        while j < data_api.get_num_trans_in_bioassembly(i):
            struct_inflator.set_bio_assembly_trans(i + 1, data_api.get_chain_index_list_for_transform(i, j), data_api.get_matrix_for_transform(i, j))
            j += 1
        i += 1




def add_inter_group_bonds(data_api, struct_inflator):
    """	 Generate inter group bonds.
	 Bond indices are specified within the whole structure and start at 0.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object"""
    for i in range(len(data_api.get_inter_group_bond_orders())):
        struct_inflator.set_inter_group_bond(data_api.get_inter_group_bond_indices()[i * 2], data_api.get_inter_group_bond_indices()[i * 2 + 1], data_api.get_inter_group_bond_orders()[i])



def add_header_info(data_api, struct_inflator):
    """ Add ancilliary header information to the structure.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object
	 """
    struct_inflator.set_header_info(data_api.get_rfree(), data_api.get_rwork(), data_api.get_resolution(), data_api.get_title(), data_api.get_deposition_date(), data_api.get_release_date(), data_api.get_experimental_methods())


def add_xtalographic_info(data_api, struct_inflator):
    """	 Add the crystallographic data to the structure.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object"""
    if data_api.get_unit_cell() != None:
        struct_inflator.set_xtal_info(data_api.get_space_group(), data_api.get_unit_cell())



def add_entity_info( data_api, struct_inflator):
    """Add the entity info to the structure.
    :param data_api the interface to the decoded data
    :param struct_inflator the interface to put the data into the client object
    """
    i = 0
    while i < data_api.get_num_entities():
        struct_inflator.set_entity_info(data_api.get_entity_chain_index_list(i), data_api.get_entity_sequence(i), data_api.get_entity_description(i), data_api.get_entity_type(i))
        i += 1
