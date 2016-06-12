import sys
def add_atom_data(data_api, data_setters, atom_names, element_names, atom_charges, atom_counter, group_atom_ind):
    """Add the atomic data to the DataTransferInterface.
    :param """
    atom_name = atom_names[group_atom_ind]
    element = element_names[group_atom_ind]
    charge = atom_charges[group_atom_ind]
    alternative_location_id = data_api.alt_id[data_api.atom_counter]
    serial_number = data_api.atom_id[data_api.atom_counter]
    x = data_api.cartnX[data_api.atom_counter]
    y = data_api.cartnY[data_api.atom_counter]
    z = data_api.cartnZ[data_api.atom_counter]
    occupancy = data_api.occupancy[data_api.atom_counter]
    temperature_factor = data_api.b_factor[data_api.atom_counter]
    data_setters.set_atom_info(atom_name, serial_number, alternative_location_id,
                               x, y, z, occupancy, temperature_factor, element, charge)


def add_group_bonds(data_setters, bond_indices, bond_orders):
    for bond_index in range(len(bond_orders)):
        data_setters.set_group_bond(bond_indices[bond_index*2],bond_indices[bond_index*2+1],bond_orders[bond_index])


def add_group(data_api, data_setters, group_ind):
    group_type_ind = data_api.group_list[group_ind]
    atom_count = len(data_api.group_map[group_type_ind]["atomNameList"])
    current_group_number = data_api.group_list[group_ind]
    insertion_code = data_api.insertion_code_list[group_ind]
    data_setters.set_group_info(data_api.group_map[group_type_ind]["groupName"],
                                data_api.group_num[group_ind], insertion_code,
                                data_api.group_map[group_type_ind]["chemCompType"],
                                atom_count, data_api.num_bonds,
                                data_api.group_map[group_type_ind]["singleLetterCode"],
                                data_api.seq_res_group_list[group_ind],
                                data_api.sec_struct_info[group_ind])
    for group_atom_ind in range(atom_count):
        add_atom_data(data_api, data_setters,
                      data_api.group_map[group_type_ind]["atomNameList"],
                      data_api.group_map[group_type_ind]["elementList"],
                      data_api.group_map[group_type_ind]["formalChargeList"],
                      data_api.atom_counter, group_atom_ind)
        data_api.atom_counter +=1
    add_group_bonds(data_setters,
                    data_api.group_map[group_type_ind]["bondAtomList"],
                    data_api.group_map[group_type_ind]["bondOrderList"])
    return atom_count


def add_chain_info(data_api, data_setters, chain_index):
    chain_id = data_api.chain_list[chain_index]
    chain_name = data_api.public_chain_ids[chain_index]
    num_groups = data_api.groups_per_chain[chain_index]
    data_setters.set_chain_info(chain_id, chain_name, num_groups)
    next_ind = data_api.group_counter + num_groups
    last_ind = data_api.group_counter
    for group_ind in range(last_ind, next_ind):
        add_group(data_api, data_setters, group_ind)
        data_api.group_counter +=1
    data_api.chain_counter+=1


def add_atomic_information(data_api, data_setters):
    for model_chains in data_api.chains_per_model:
        data_setters.set_model_info(data_api.model_counter, model_chains)
        tot_chains_this_model = data_api.chain_counter + model_chains
        last_chain_counter = data_api.chain_counter
        for chain_index in range(last_chain_counter, tot_chains_this_model):
            add_chain_info(data_api, data_setters, chain_index)
        data_api.model_counter+=1


def generate_bio_assembly(data_api, struct_inflator):
    """Generate the bioassembly data.
    :param data_api the interface to the decoded data
    :param struct_inflator the interface to put the data into the client object"""
    bioassembly_count = 0
    for bioassembly in data_api.bio_assembly:
        bioassembly_count += 1
        for transform in bioassembly[b"transformList"]:
            struct_inflator.set_bio_assembly_trans(bioassembly_count,
                                                   transform[b"chainIndexList"],
                                                   transform[b"matrix"])

def add_inter_group_bonds(data_api, struct_inflator):
    """	 Generate inter group bonds.
	 Bond indices are specified within the whole structure and start at 0.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object"""
    for i in range(len(data_api.inter_group_bond_orders)):
        struct_inflator.set_inter_group_bond(data_api.inter_group_bond_indices[i * 2],
                                             data_api.inter_group_bond_indices[i * 2 + 1],
                                             data_api.inter_group_bond_orders[i])



def add_header_info(data_api, struct_inflator):
    """ Add ancilliary header information to the structure.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object
	 """
    struct_inflator.set_header_info(data_api.r_free,
                                    data_api.r_work,
                                    data_api.resolution,
                                    data_api.title,
                                    data_api.deposition_date,
                                    data_api.release_date,
                                    data_api.experimental_methods)



def add_xtalographic_info(data_api, struct_inflator):
    """	 Add the crystallographic data to the structure.
	 :param data_api the interface to the decoded data
	 :param struct_inflator the interface to put the data into the client object"""
    if data_api.unit_cell != None:
        struct_inflator.set_xtal_info(data_api.space_group,
                                      data_api.unit_cell)



def add_entity_info( data_api, struct_inflator):
    """Add the entity info to the structure.
    :param data_api the interface to the decoded data
    :param struct_inflator the interface to put the data into the client object
    """
    for entity in data_api.entity_list:
        struct_inflator.set_entity_info(entity[b"chainIndexList"],
                                        entity[b"sequence"],
                                        entity[b"description"],
                                        entity[b"type"])

def decode_entity_list(input_data):
    """Convert byte strings to strings in the entity list.
    :param input_data the list of entities
    :return the decoded entity list"""
    if sys.version_info[0] < 3:
        return input_data
    out_data = []
    for entry in input_data:
        out_data.append(convert_entity(entry))
    return out_data

def decode_group_map(input_data):
    """Convert byte strings to strings in the group map.
    :param input_data the list of groups
    :return the decoded group list"""
    if sys.version_info[0] < 3:
        return input_data
    out_data = []
    for entry in input_data:
        out_data.append(convert_group(entry))
    return out_data

def convert_group(input_group):
    """Convert an individual group from byte strings to regula strings.
    :param input_group the input group
    :return the decoded group"""
    output_group = {}
    for key in input_group:
        if key in [b'elementList',b'atomNameList']:
            output_group[key.decode('ascii')] = [x.decode('ascii') for x in input_group[key]]
        elif key in [b'chemCompType',b'groupName',b'singleLetterCode']:
            output_group[key.decode('ascii')] = input_group[key].decode('ascii')
        else:
            output_group[key.decode('ascii')] = input_group[key]
    return output_group

def convert_entity(input_entity):
    """Convert an individual entity from byte strings to regular strings
    :param input_entity the entity to decode
    :return the decoded entity"""
    output_entity  = {}
    for key in input_entity:
        if key in [ b'description', b'type', b'sequence']:
            output_entity[key.decode('ascii')] = input_entity[key].decode('ascii')
        else:
            output_entity[key.decode('ascii')] = input_entity[key]
    return output_entity