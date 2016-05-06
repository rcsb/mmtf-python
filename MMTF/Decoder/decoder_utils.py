


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
