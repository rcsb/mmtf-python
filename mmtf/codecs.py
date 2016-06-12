from mmtf import converters, decoders,encoders
import mmtf,struct

def parse_header(input_array):
    """Parse the header and return it along with the input array minus the header.
    :param input_array the array to parse
    :return the codec, the length of the decoded array, the parameter and the remainder
    of the array"""
    codec = struct.unpack(mmtf.NUM_DICT[4], input_array[0:4])[0]
    length = struct.unpack(mmtf.NUM_DICT[4], input_array[4:8])[0]
    param = struct.unpack(mmtf.NUM_DICT[4], input_array[8:12])[0]
    return codec,length,param,input_array[12:]


def add_header(input_array, codec, length, param):
    """Add the header to the appropriate array.
    :param the encoded array to add the header to
    :param the codec being used
    :param the length of the decoded array
    :param the parameter to add to the header
    :return the prepended encoded byte array"""
    return struct.pack(mmtf.NUM_DICT[4],codec)+\
           struct.pack(mmtf.NUM_DICT[4],length)+\
           struct.pack(mmtf.NUM_DICT[4],param)+input_array

class DeltaRecursiveFloat():
    """Covert an array of floats to integers, perform delta
    encoding and then use recursive indexing to store as 2
    byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(
            decoders.delta_decode(
                converters.recursive_index_decode(
                    converters.convert_bytes_to_ints(in_array,2))),param)
    @staticmethod
    def encode(in_array, param):
        return converters.convert_ints_to_bytes(
            converters.recursive_index_encode(
                encoders.delta_encode(
                    converters.convert_floats_to_ints(in_array,param))),2)

class RunLengthFloat():
    """Covert an array of floats to integers, perform run-length
    encoding and then store as four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(in_array,4)),param)
    @staticmethod
    def encode(in_array,param):
        return converters.convert_ints_to_bytes(
            encoders.run_length_encode(
                converters.convert_floats_to_ints(in_array,param)),4)

class RunLengthDeltaInt():
    """Delta encode an array of integers and then perform run-length
    encoding on this and then store as four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return decoders.delta_decode(
            decoders.run_length_decode(
                converters.convert_bytes_to_ints(in_array, 4)))
    @staticmethod
    def encode(in_array,param):
        return converters.convert_ints_to_bytes(
            encoders.run_length_encode(
                encoders.delta_encode(in_array)),4)

class RunLengthChar():
    """Convert chars to integers and run-length encoode these and then store as
    four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_chars(
            decoders.run_length_decode(
                converters.convert_bytes_to_ints(in_array, 4)))
    @staticmethod
    def encode(in_array, param):
        return converters.convert_ints_to_bytes(
            encoders.run_length_encode(
                converters.convert_chars_to_ints(in_array)),4)

class EncodeString():
    """Convert strings to set length byte arrays (in this case four). If
    a string is of lenght less than four a null byte is used instead."""
    @staticmethod
    def decode(in_array,param):
        return converters.decode_chain_list(in_array)
    @staticmethod
    def encode(in_array,param):
        return converters.encode_chain_list(in_array)


class ByteToInt():
    """Convert integers to single bytes and store in byte array."""
    @staticmethod
    def decode(in_array,param):
        return converters.convert_bytes_to_ints(in_array, 1)
    @staticmethod
    def encode(in_array,param):
        return converters.convert_ints_to_bytes(in_array,1)


class FourByteToInt():
    """Convert integers to four bytes and store in byte array."""
    @staticmethod
    def decode(in_array,param):
        return converters.convert_bytes_to_ints(in_array, 4)
    @staticmethod
    def encode(in_array, param):
        return converters.convert_ints_to_bytes(in_array, 4)

codec_dict = {10: DeltaRecursiveFloat,
                9: RunLengthFloat,
                8: RunLengthDeltaInt,
                6: RunLengthChar,
                5: EncodeString,
                2: ByteToInt,
                4: FourByteToInt}

def decode_array(input_array):
    """Parse the header of an input byte array and then decode using the input array,
    the codec and the appropirate parameter"""
    codec,length,param,input_array = parse_header(input_array)
    return codec_dict[codec].decode(input_array,param)

def encode_array(input_array, codec, param):
    """Encode the array using the method and then add the header to this array"""
    return add_header(codec_dict[codec].encode(input_array,param),codec,len(input_array),param)
