from mmtf import converters, decoders
import mmtf,struct

def parse_header(input_array):
    """Parse the header and return it along with the input array minus the header"""
    codec = struct.unpack(mmtf.NUM_DICT[4], input_array[0:4])[0]
    length = struct.unpack(mmtf.NUM_DICT[4], input_array[4:8])[0]
    param = struct.unpack(mmtf.NUM_DICT[4], input_array[8:12])[0]
    return codec,length,param,input_array[12:]

class DeltaRecursiveFloat():
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(decoders.delta_decode(converters.recursive_index_decode(converters.convert_bytes_to_ints(in_array,2))),
                                                 param)

class RunLengthFloat():
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_floats(
                decoders.run_length_decode(converters.convert_bytes_to_ints(in_array,4)),param)

class RunLengthDeltaInt():
    @staticmethod
    def decode(in_array, param):
        return decoders.delta_decode(
            decoders.run_length_decode(
                converters.convert_bytes_to_ints(in_array, 4)))

class RunLengthChar():
    @staticmethod
    def decode(in_array, param):
        return converters.convert_ints_to_chars(
                decoders.run_length_decode(
                    converters.convert_bytes_to_ints(in_array, 4)))


class EncodeString():
    @staticmethod
    def decode(in_array,param):
        return converters.decode_chain_list(in_array)


class ByteToInt():
    @staticmethod
    def decode(in_array,param):
        return converters.convert_bytes_to_ints(in_array, 1)

class FourByteToInt():
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
    codec,length,param,input_array = parse_header(input_array)
    print codec
    return decoder_dict[codec].decode(input_array,param)
