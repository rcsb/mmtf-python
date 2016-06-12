import unittest

import msgpack

from mmtf import converters,decoders,encoders

from mmtf import codecs,fetch,parse,parse_gzip
from mmtf import MMTFDecoder


def run_all(unit_test, encoded_data, decoded_data, param, codec_id):
    """Test that a given codec can work in the forward backward and round trip both ways."""
    unit_test.assertEqual(codecs.codec_dict[codec_id].decode(encoded_data, param), decoded_data)
    unit_test.assertEqual(codecs.codec_dict[codec_id].encode(decoded_data, param), encoded_data)
    unit_test.assertEqual(codecs.codec_dict[codec_id].encode(codecs.codec_dict[codec_id].decode(encoded_data, param),
                                                             param), encoded_data)
    unit_test.assertEqual(codecs.codec_dict[codec_id].decode(codecs.codec_dict[codec_id].encode(decoded_data, param),
                                                         param), decoded_data)

class CodecTest(unittest.TestCase):
    def test_delt_rec_float(self):
        test_data = b'\x7f\xffD\xab\x01\x8f\xff\xca'
        output_data = [50.346, 50.745, 50.691]
        run_all(self, test_data, output_data, 1000, 10)
    def test_run_len_float(self):
        test_data = b'\x00\x00\x00d\x00\x00\x00\x03'
        output_data = [1.00,1.00,1.00]
        run_all(self, test_data, output_data, 100, 9)

    def test_run_len_delta_int(self):
        test_data = b'\x00\x00\x00\x01\x00\x00\x00\x07'
        output_data = [1,2,3,4,5,6,7]
        run_all(self, test_data, output_data, 0, 8)

    def test_run_len_char(self):
        test_data = b'\x00\x00\x00\x41\x00\x00\x00\x04'
        output_data = ["A","A","A","A"]
        run_all(self, test_data, output_data, 0, 6)

    def test_enc_str(self):
        test_data = b'B\x00\x00\x00A\x00\x00\x00C\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00'
        output_data =  ["B","A","C","A","A","A"]
        run_all(self, test_data, output_data, 0, 5)

    def test_byte_to_int(self):
        test_data =  b'\x07\x06\x06\x07\x07'
        output_data = [7,6,6,7,7]
        run_all(self, test_data, output_data, 0, 2)

    def test_four_byte_int(self):
        test_data = b'\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        output_data = [1, 131073, 0, 2]
        run_all(self, test_data, output_data, 0, 4)

class DecoderTests(unittest.TestCase):
    def test_run_length_decode(self):
        input_data = [15,3,100,2,111,4,10000,6]
        output_data_test = [15,15,15,100,100,111,111,111,111,10000,10000,10000,10000,10000,10000]
        output_data = decoders.run_length_decode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_run_length_decode(self):
        input_data = []
        output_data_test = []
        output_data = decoders.run_length_decode(input_data)
        self.assertEqual(output_data, output_data_test)


    def test_delta_decode(self):
        input_data = [15,3,100,-1,11,4]
        output_data_test = [15,18,118,117,128,132]
        output_data = decoders.delta_decode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_delta_decode(self):
        input_data = []
        output_data_test = []
        output_data = decoders.delta_decode(input_data)
        self.assertEqual(output_data, output_data_test)

class EncoderTests(unittest.TestCase):
    def test_run_length_encode(self):
        output_data_test = [15, 3, 100, 2, 111, 4, 10000, 6]
        input_data = [15, 15, 15, 100, 100, 111, 111, 111, 111, 10000, 10000, 10000, 10000, 10000, 10000]
        output_data = encoders.run_length_encode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_run_length_encode(self):
        input_data = []
        output_data_test = []
        output_data = encoders.run_length_encode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_delta_encode(self):
        output_data_test = [15, 3, 100, -1, 11, 4]
        input_data = [15, 18, 118, 117, 128, 132]
        output_data = encoders.delta_encode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_delta_decode(self):
        input_data = []
        output_data_test = []
        output_data = encoders.delta_encode(input_data)
        self.assertEqual(output_data, output_data_test)


class ConverterTests(unittest.TestCase):

    def test_convert_chain_list(self):
        in_bytes = b'A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00'
        out_strings_test =  ["A", "A","A","A","A","A"]
        self.assertEqual(out_strings_test, converters.decode_chain_list(in_bytes))
        self.assertEqual(in_bytes, converters.encode_chain_list(out_strings_test))

    def test_convert_int_to_float(self):
        in_array = [10001,100203,124542]
        out_array_test = [10.001,100.203,124.542]
        self.assertEqual(out_array_test, converters.convert_ints_to_floats(in_array, 1000.0))
        self.assertEqual(in_array, converters.convert_floats_to_ints(out_array_test, 1000.0))

    def test_recursive_enc(self):
        in_arr = [1,420,32767,120,-32768,34767]
        out_array_test = [1,420,32767,0,120,-32768,0,32767,2000]
        self.assertEqual(out_array_test, converters.recursive_index_encode(in_arr))

    def test_recursive_dec(self):
        in_arr = [1,420,32767,0,120,-32768,0,32767,2000]
        out_array_test = [1,420,32767,120,-32768,34767]
        self.assertEqual(out_array_test, converters.recursive_index_decode(in_arr))

    def test_recursive_round(self):
        in_arr = [1,420,32767,120,-32768,34767]
        self.assertEqual(in_arr, converters.recursive_index_decode(converters.recursive_index_encode(in_arr)))

    def test_convert_one_byte_int(self):
        in_bytes = b'\x07\x06\x06\x07\x07'
        out_array_test = [7,6,6,7,7]
        self.assertEqual(out_array_test, converters.convert_bytes_to_ints(in_bytes,1))
        self.assertEqual(in_bytes, converters.convert_ints_to_bytes(out_array_test,1))
        self.assertEqual(in_bytes,converters.convert_ints_to_bytes(converters.convert_bytes_to_ints(in_bytes,1),1))

    def test_convert_two_byte_int(self):
        in_bytes = b'\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        out_array_test = [0,1,2,1,0,0,0,2]
        self.assertEqual(out_array_test, converters.convert_bytes_to_ints(in_bytes,2))
        self.assertEqual(in_bytes, converters.convert_ints_to_bytes(out_array_test, 2))
        self.assertEqual(in_bytes,converters.convert_ints_to_bytes(converters.convert_bytes_to_ints(in_bytes,2),2))


    def test_convert_four_byte_int(self):
        in_bytes = b'\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        out_array_test = [1, 131073, 0, 2]
        self.assertEqual(out_array_test, converters.convert_bytes_to_ints(in_bytes,4))
        self.assertEqual(in_bytes, converters.convert_ints_to_bytes(out_array_test,4))
        self.assertEqual(in_bytes,converters.convert_ints_to_bytes(converters.convert_bytes_to_ints(in_bytes,4),4))

    def test_parse_header(self):
        in_bytes = b'\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        codec,length,param, bytearray = codecs.parse_header(in_bytes)
        self.assertEqual(length,131073)
        self.assertEqual(param,0)
        self.assertEqual(len(bytearray),4)

    def test_convert_int_to_char(self):
        int_array =  [66,63,67]
        out_array_test = ["B", "?","C"]
        self.assertEqual(out_array_test, converters.convert_ints_to_chars(int_array))
        self.assertEqual(int_array, converters.convert_chars_to_ints(out_array_test))

    def test_encoder(self):
        decoded = parse("mmtf/tests/testdatastore/4CUP.mmtf")
        decoded.encode_data()

    def test_decoder(self):
        decoded = parse("mmtf/tests/testdatastore/4CUP.mmtf")

    def test_gz_decoder(self):
        decoded = parse_gzip("mmtf/tests/testdatastore/4CUP.mmtf.gz")

    def test_round_trip(self):
        decoded = parse("mmtf/tests/testdatastore/4CUP.mmtf")
        packed = decoded.get_msgpack()
        decoded.decode_data(msgpack.unpackb(packed))

    def test_gzip_open(self):
        from mmtf import ungzip_data
        ungzip_data(open("mmtf/tests/testdatastore/4CUP.mmtf.gz","rb").read())

    def test_fetch(self):
        decoded = fetch("4CUP")

if __name__ == '__main__':
    unittest.main()
