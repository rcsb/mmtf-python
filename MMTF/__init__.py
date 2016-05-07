import gzip
import time
import urllib2
from StringIO import StringIO
from abc import ABCMeta, abstractmethod

import msgpack

from mmtf import converters, decoders, decoder_utils

COORD_DIVIDER = 1000.0
OCC_B_FACTOR_DIVIDER = 100.0
MAX_SHORT = 32767
NULL_BYTE = '\x00'
CHAIN_LEN = 4
NUM_DICT = {1:'b',2:'>h',4:'>i'}
BASE_URL = "http://mmtf.rcsb.org/v0/full/"

class MMTFDecoder():
    """Class to decode raw mmtf data into a parsed data model that can be fed into
    other data model"""
    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0

    def decode_data(self, input_data):
        self.group_list = converters.convert_bytes_to_ints(input_data["groupTypeList"], 4)
        # Decode the coordinate  and B-factor arrays.
        self.cartnX = converters.convert_ints_to_floats(
            decoders.delta_decode(
                converters.combine_integers(
                    converters.convert_bytes_to_ints(input_data["xCoordSmall"], 2),
                    converters.convert_bytes_to_ints(input_data["xCoordBig"], 4))),
            COORD_DIVIDER )
        self.cartnY = converters.convert_ints_to_floats(
            decoders.delta_decode(
                converters.combine_integers(
                    converters.convert_bytes_to_ints(
                        input_data["yCoordSmall"],2),
                    converters.convert_bytes_to_ints(input_data["yCoordBig"], 4))),
            COORD_DIVIDER )
        self.cartnZ = converters.convert_ints_to_floats(
            decoders.delta_decode(
                converters.combine_integers(
                    converters.convert_bytes_to_ints(
                        input_data["zCoordSmall"],2),
                    converters.convert_bytes_to_ints(input_data["zCoordBig"], 4))),
            COORD_DIVIDER)
        # Run length decode the occupancy array
        if "bFactorSmall" in input_data and "bFactorBig" in input_data:
            self.b_factor = converters.convert_ints_to_floats(
                decoders.delta_decode(
                    converters.combine_integers(
                        converters.convert_bytes_to_ints(input_data["bFactorSmall"], 2),
                        converters.convert_bytes_to_ints(input_data["bFactorBig"], 4))),
                OCC_B_FACTOR_DIVIDER)
        else:
            self.b_factor = []
        if "occupancyList" in input_data:
            self.occupancy = converters.convert_ints_to_floats(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(
                        input_data["occupancyList"],4)),
                OCC_B_FACTOR_DIVIDER)
        else:
            self.occupancy = []
        # Run length and delta
        if "atomIdList" in input_data:
            self.atom_id = decoders.delta_decode(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(input_data["atomIdList"], 4)))
        else:
            self.atom_id = []
        # Run length encoded
        if "altLocList" in input_data:
            self.alt_id = converters.convert_ints_to_chars(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(input_data["altLocList"], 4)))
        else:
            self.alt_id = []
        if "insCodeList" in input_data:
            self.insertion_code_list = converters.convert_ints_to_chars(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(input_data["insCodeList"], 4)))
        else:
            self.insertion_code_list = []
        # Get the group_number
        self.group_num = decoders.delta_decode(
            decoders.run_length_decode(
                converters.convert_bytes_to_ints(input_data["groupIdList"], 4)))
        # Get the group map (all the unique groups in the structure).
        self.group_map = input_data["groupList"]
        # Get the seq_res groups
        if "sequenceIndexList" in input_data:
            self.seq_res_group_list = decoders.delta_decode(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(input_data["sequenceIndexList"], 4)))
        else:
            self.seq_res_group_list = []
        # Get the number of chains per model
        self.chains_per_model = input_data["chainsPerModel"]
        self.groups_per_chain = input_data["groupsPerChain"]
        # Get the internal and public facing chain ids
        if "chainNameList" in input_data:
            self.public_chain_ids = converters.decode_chain_list(input_data["chainNameList"])
        else:
            self.public_chain_ids = []
        self.chain_list = converters.decode_chain_list(input_data["chainIdList"])
        self.space_group = input_data["spaceGroup"]
        self.inter_group_bond_indices = converters.convert_bytes_to_ints(input_data["bondAtomList"], 4)
        self.inter_group_bond_orders = converters.convert_bytes_to_ints(input_data["bondOrderList"], 1)
        self.mmtf_version = input_data["mmtfVersion"]
        self.mmtf_producer = input_data["mmtfProducer"]
        self.structure_id = input_data["structureId"]
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

        self.sec_struct_info = converters.convert_bytes_to_ints(input_data["secStructList"], 1)

        self.num_bonds = len(self.inter_group_bond_orders)
        for in_int in self.group_list:
            self.num_bonds += len(self.group_map[in_int]["bondOrderList"])

        self.num_chains = len(self.chain_list)
        self.num_models = len(self.chains_per_model)
        self.num_atoms = len(self.cartnY)
        self.num_groups = len(self.group_list)

    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters
        :type data_setters: DataTransferInterface
        """
        data_setters.init_structure(self.num_bonds, len(self.cartnX), len(self.group_list),
                                   len(self.chain_list), len(self.chains_per_model), self.structure_id)
        # Set the entity information
        decoder_utils.add_entity_info(self, data_setters)
        # First add the atomic data
        decoder_utils.add_atomic_information(self, data_setters)
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


def get_raw_data_from_url(pdb_id):
    """" Get the msgpack unpacked data given a PDB id.
    :param the input PDB id
    :return the unpacked data (a dict) """
    url = BASE_URL + pdb_id
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    out_data = msgpack.unpackb(data)
    return out_data


def fetch(pdb_id):
    """Return a decoded API to the data from a PDB id
    :param the input PDB id
    :return an API to decoded data """
    timeOne = time.time()
    decoder = MMTFDecoder()
    decoder.decode_data(get_raw_data_from_url(pdb_id))
    return decoder