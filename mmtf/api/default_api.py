import gzip

from mmtf.utils.constants import BASE_URL
try:
    import urllib2
    from StringIO import StringIO
except:
    import urllib.request as urllib2
    from io import BytesIO as StringIO
import msgpack,sys
from mmtf.codecs import decode_array, encode_array
from mmtf.utils import decoder_utils


class MMTFDecoder():
    """Class to decode raw mmtf data into a parsed data model that can be fed into other data model"""
    model_counter = 0
    chain_counter = 0
    group_counter = 0
    atom_counter = 0
    def decode_data(self, input_data):
        """Function to decode the input data and place it onto the class.

        :param input_data: the input data as a dict"""
        self.group_type_list = decode_array(input_data[b"groupTypeList"])
        self.x_coord_list = decode_array(input_data[b"xCoordList"])
        self.y_coord_list = decode_array(input_data[b"yCoordList"])
        self.z_coord_list = decode_array(input_data[b"zCoordList"])
        if b"bFactorList" in input_data:
            self.b_factor_list = decode_array(input_data[b"bFactorList"])
        else:
            self.b_factor_list = []
        if b"occupancyList" in input_data:
            self.occupancy_list = decode_array(input_data[b"occupancyList"])
        else:
            self.occupancy_list = []
        if b"atomIdList" in input_data:
            self.atom_id_list = decode_array(input_data[b"atomIdList"])
        else:
            self.atom_id_list = []
        if b"altLocList" in input_data:
            self.alt_loc_list = decode_array(input_data[b"altLocList"])
        else:
            self.alt_loc_list = []
        if b"insCodeList" in input_data:
            self.ins_code_list = decode_array(input_data[b"insCodeList"])
        else:
            self.ins_code_list = []
        self.group_id_list = decode_array(input_data[b"groupIdList"])
        self.group_list = decoder_utils.decode_group_map(input_data[b"groupList"])
        if b"sequenceIndexList" in input_data:
            self.sequence_index_list = decode_array(input_data[b"sequenceIndexList"])
        else:
            self.sequence_index_list = []
        self.chains_per_model = input_data[b"chainsPerModel"]
        self.groups_per_chain = input_data[b"groupsPerChain"]
        if b"chainNameList" in input_data:
            self.chain_name_list = decode_array(input_data[b"chainNameList"])
        else:
            self.chain_name_list = []
        self.chain_id_list = decode_array(input_data[b"chainIdList"])
        self.space_group = input_data[b"spaceGroup"]
        self.bond_atom_list = decode_array(input_data[b"bondAtomList"])
        self.bond_order_list = decode_array(input_data[b"bondOrderList"])
        if sys.version_info[0] < 3:
            self.mmtf_version = input_data[b"mmtfVersion"]
            self.mmtf_producer = input_data[b"mmtfProducer"]
            self.structure_id = input_data[b"structureId"]
        else:
            self.mmtf_version = input_data[b"mmtfVersion"].decode('ascii')
            self.mmtf_producer = input_data[b"mmtfProducer"].decode('ascii')
            self.structure_id = input_data[b"structureId"].decode('ascii')

        if b"title" in input_data:
            if sys.version_info[0] < 3:
                self.title = input_data[b"title"]
            else:
                self.title = input_data[b"title"].decode('ascii')
        if b"experimentalMethods" in input_data:
            if sys.version_info[0] < 3:
                self.experimental_methods = [x.decode('ascii') for x in input_data[b"experimentalMethods"]]
            else:
                self.experimental_methods = input_data[b"experimentalMethods"]
        else:
            self.experimental_methods = None
        if b"depositionDate" in input_data:
            if sys.version_info[0] < 3:
                self.deposition_date = input_data[b"depositionDate"]
            else:
                self.deposition_date = input_data[b"depositionDate"].decode('ascii')
        else:
            self.deposition_date = None
        if b"releaseDate" in input_data:
            if sys.version_info[0] < 3:
                self.release_date = input_data[b"releaseDate"]
            else:
                self.release_date = input_data[b"releaseDate"].decode('ascii')
        else:
            self.release_date = None
        if b"entityList" in input_data:
            self.entity_list = decoder_utils.decode_entity_list(input_data[b"entityList"])
        else:
            self.entity_list = []
        if b"bioAssemblyList" in input_data:
            self.bio_assembly = input_data[b"bioAssemblyList"]
        else:
            self.bio_assembly = []
        if b"rFree" in input_data:
            self.r_free = input_data[b"rFree"]
        else:
            self.r_free = None
        if b"rWork" in input_data:
            self.r_work = input_data[b"rWork"]
        else:
            self.r_work = None
        if b"resolution" in input_data:
            self.resolution = input_data[b"resolution"]
        if b"unitCell" in input_data:
            self.unit_cell = input_data[b"unitCell"]
        else:
            self.unit_cell = None
        self.sec_struct_list = decode_array(input_data[b"secStructList"])
        self.num_bonds = int(input_data[b"numBonds"])
        self.num_chains = int(input_data[b"numChains"])
        self.num_models = int(input_data[b"numModels"])
        self.num_atoms = int(input_data[b"numAtoms"])
        self.num_groups = int(input_data[b"numGroups"])

    def encode_data(self):
        """Encode the data back into a dict."""
        output_data = {}
        output_data[b"groupTypeList"] = encode_array(self.group_type_list, 2, 0)
        output_data[b"xCoordList"] = encode_array(self.x_coord_list, 10, 1000)
        output_data[b"yCoordList"] = encode_array(self.y_coord_list, 10, 1000)
        output_data[b"zCoordList"] = encode_array(self.z_coord_list, 10, 1000)
        output_data[b"bFactorList"] = encode_array(self.b_factor_list, 10, 100)
        output_data[b"occupancyList"] = encode_array(self.occupancy_list, 9, 100)
        output_data[b"atomIdList"] = encode_array(self.atom_id_list, 8, 0)
        output_data[b"altLocList"] = encode_array(self.alt_loc_list, 6, 0)
        output_data[b"insCodeList"] = encode_array(self.ins_code_list, 6, 0)
        output_data[b"groupIdList"] = encode_array(self.group_id_list, 4, 0)
        output_data[b"groupList"] = self.group_list
        output_data[b"sequenceIndexList"] = encode_array(self.sequence_index_list, 8, 0)
        output_data[b"chainNameList"] = encode_array(self.chain_name_list, 5, 0)
        output_data[b"chainIdList"] = encode_array(self.chain_id_list, 5, 0)
        output_data[b"bondAtomList"] = encode_array(self.bond_atom_list, 4, 0)
        output_data[b"bondOrderList"] =  encode_array(self.bond_order_list, 2, 0)
        output_data[b"secStructList"] = encode_array(self.sec_struct_list, 2, 0)
        output_data[b"chainsPerModel"] = self.chains_per_model
        output_data[b"groupsPerChain"] = self.groups_per_chain
        output_data[b"spaceGroup"] = self.space_group
        output_data[b"mmtfVersion"] = self.mmtf_version
        output_data[b"mmtfProducer"] = self.mmtf_producer
        output_data[b"structureId"] = self.structure_id
        output_data[b"entityList"] = self.entity_list
        output_data[b"bioAssemblyList"] = self.bio_assembly
        output_data[b"rFree"] = self.r_free
        output_data[b"rWork"] = self.r_work
        output_data[b"resolution"] = self.resolution
        output_data[b"title"] = self.title
        output_data[b"experimentalMethods"] = self.experimental_methods
        output_data[b"depositionDate"] = self.deposition_date
        output_data[b"releaseDate"] = self.release_date
        output_data[b"unitCell"] = self.unit_cell
        output_data[b"numBonds"] = self.num_bonds
        output_data[b"numChains"] = self.num_chains
        output_data[b"numModels"] = self.num_models
        output_data[b"numAtoms"] = self.num_atoms
        output_data[b"numGroups"]= self.num_groups
        return output_data


    def pass_data_on(self, data_setters):
        """Write the data from the getters to the setters.

        :param data_setters: a series of functions that can fill a chemical
        data structure
        :type data_setters: DataTransferInterface
        """
        data_setters.init_structure(self.num_bonds, len(self.x_coord_list), len(self.group_type_list),
                                    len(self.chain_id_list), len(self.chains_per_model), self.structure_id)
        decoder_utils.add_entity_info(self, data_setters)
        decoder_utils.add_atomic_information(self, data_setters)
        decoder_utils.add_header_info(self, data_setters)
        decoder_utils.add_xtalographic_info(self, data_setters)
        decoder_utils.generate_bio_assembly(self, data_setters)
        decoder_utils.add_inter_group_bonds(self, data_setters)
        data_setters.finalize_structure()

    def get_msgpack(self):
        """Get the msgpack of the encoded data."""
        return msgpack.packb(self.encode_data())

def get_raw_data_from_url(pdb_id):
    """" Get the msgpack unpacked data given a PDB id.

    :param pdb_id: the input PDB id
    :return the unpacked data (a dict) """
    url = BASE_URL + pdb_id
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)
    if response.info().get('Content-Encoding') == 'gzip':
        data = ungzip_data(response.read())
    return _unpack(data)


def _unpack(data):
    out_data = msgpack.unpackb(data.read())
    return out_data


def fetch(pdb_id):
    """Return a decoded API to the data from a PDB id.

    :param pdb_id: the input PDB id
    :return an API to decoded data """
    decoder = MMTFDecoder()
    decoder.decode_data(get_raw_data_from_url(pdb_id))
    return decoder

def parse(file_path):
    """Return a decoded API to the data from a file path.

    :param file_path: the input file path. Data is not entropy compressed (e.g. gzip)
    :return an API to decoded data """
    newDecoder = MMTFDecoder()
    newDecoder.decode_data(msgpack.unpackb(open(file_path, "rb").read()))
    return newDecoder


def parse_gzip(file_path):
    """Return a decoded API to the data from a file path. File is gzip compressed.
    :param file_path: the input file path. Data is gzip compressed.
    :return an API to decoded data"""
    newDecoder = MMTFDecoder()
    newDecoder.decode_data(msgpack.unpackb(gzip.open(file_path, "rb").read()))
    return newDecoder


def ungzip_data(input_data):
    """Retrun a string of data after gzip decoding

    :param the input gziped data
    :return  the gzip decoded data"""
    buf = StringIO(input_data)
    f = gzip.GzipFile(fileobj=buf)
    return f
