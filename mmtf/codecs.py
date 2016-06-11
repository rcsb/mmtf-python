from mmtf import converters, decoders
import mmtf,struct

def parse_header(input_array):
    """Parse the header and return it along with the input array minus the header"""
    codec = struct.unpack(mmtf.NUM_DICT[4], input_array[0:4])[0]
    length = struct.unpack(mmtf.NUM_DICT[4], input_array[4:8])[0]
    param = struct.unpack(mmtf.NUM_DICT[4], input_array[8:12])[0]
    return codec,length,param,input_array[12:]

class DeltaRecursiveFloat():
    """Covert an array of floats to integers, perform delta
    encoding and then use recursive indexing to store as 2
    byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(decoders.delta_decode(
            converters.recursive_index_decode(
                converters.convert_bytes_to_ints(in_array,2))),
                                                 param)

class RunLengthFloat():
    """Covert an array of floats to integers, perform run-length
    encoding and then store as four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(
                decoders.run_length_decode(converters.convert_bytes_to_ints(in_array,4)),param)

class RunLengthDeltaInt():
    """Delta encode an array of integers and then perform run-length
    encoding on this and then store as four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        return decoders.delta_decode(
            decoders.run_length_decode(
                converters.convert_bytes_to_ints(in_array, 4)))

class RunLengthChar():
    """Convert chars to integers and run-length encoode these and then store as
    four byte integers in a byte array."""
    @staticmethod
    def decode(in_array, param):
        ints = converters.convert_bytes_to_ints(in_array, 4)
        print(ints)
        rlInts = decoders.run_length_decode(ints)
        print(rlInts)
        decoded = converters.convert_ints_to_chars(rlInts)
        print(rlInts)
        return decoded

class EncodeString():
    """Convert strings to set length byte arrays (in this case four). If
    a string is of lenght less than four a null byte is used instead."""
    @staticmethod
    def decode(in_array,param):
        return converters.decode_chain_list(in_array)


class ByteToInt():
    """Convert integers to single bytes and store in byte array."""
    @staticmethod
    def decode(in_array,param):
        return converters.convert_bytes_to_ints(in_array, 1)

class FourByteToInt():
    """Convert integers to four bytes and store in byte array."""
    @staticmethod
    def decode(in_array,param):
        return converters.convert_bytes_to_ints(in_array, 4)

decoder_dict = {10: DeltaRecursiveFloat,
                9: RunLengthFloat,
                8: RunLengthDeltaInt,
                6: RunLengthChar,
                5: EncodeString,
                4: ByteToInt,
                2: FourByteToInt}

def decode_array(input_array):
    """Parse the header of an input byte array and then decode using the input array,
    the codec and the appropirate parameter"""
    codec,length,param,input_array = parse_header(input_array)
    return decoder_dict[codec].decode(input_array,param)
