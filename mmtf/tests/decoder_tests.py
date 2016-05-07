import unittest

import msgpack

import mmtf.converters as ac
import mmtf.decoders as ad
from mmtf import MMTFDecoder


class DecoderTests(unittest.TestCase):
    def test_run_length_decode(self):
        input_data = [15,3,100,2,111,4,10000,6]
        output_data_test = [15,15,15,100,100,111,111,111,111,10000,10000,10000,10000,10000,10000]
        output_data = ad.run_length_decode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_run_length_decode(self):
        input_data = []
        output_data_test = []
        output_data = ad.run_length_decode(input_data)
        self.assertEqual(output_data, output_data_test)


    def test_delta_decode(self):
        input_data = [15,3,100,-1,11,4]
        output_data_test = [15,18,118,117,128,132]
        output_data = ad.delta_decode(input_data)
        self.assertEqual(output_data, output_data_test)

    def test_empty_delta_decode(self):
        input_data = []
        output_data_test = []
        output_data = ad.delta_decode(input_data)
        self.assertEqual(output_data, output_data_test)

class ConvrterTests(unittest.TestCase):

    def test_convert_chain_list(self):
        in_bytes = 'A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00A\x00\x00\x00'
        out_strings_test =  ["A", "A","A","A","A","A"]
        self.assertEqual(out_strings_test, ac.decode_chain_list(in_bytes))

    def test_convert_int_to_float(self):
        in_array = [10001,100203,124542]
        out_array_test = [10.001,100.203,124.542]
        self.assertEqual(out_array_test, ac.convert_ints_to_floats(in_array, 1000.0))


    def test_convert_one_byte_int(self):
        in_bytes = '\x07\x06\x06\x07\x07'
        out_array_test = [7,6,6,7,7]
        self.assertEqual(out_array_test, ac.convert_bytes_to_ints(in_bytes,1))


    def test_convert_two_byte_int(self):
        in_bytes = '\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        out_array_test = [0,1,2,1,0,0,0,2]
        self.assertEqual(out_array_test, ac.convert_bytes_to_ints(in_bytes,2))

    def test_convert_four_byte_int(self):
        in_bytes = '\x00\x00\x00\x01\x00\x02\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'
        out_array_test = [1, 131073, 0, 2]
        self.assertEqual(out_array_test, ac.convert_bytes_to_ints(in_bytes,4))

    def test_convert_int_to_char(self):
        int_array =  [66,63,67]
        out_array_test = ["B", "?","C"]
        self.assertEqual(out_array_test, ac.convert_ints_to_chars(int_array))

    def test_combine_integers(self):
        two_byte_int_arr = [1,2,5,4,50,0]
        four_byte_int_arr = [10002,4,1002,2]
        combined_array_test = [10002,1,2,5,4,1002,50,0]
        self.assertEqual(combined_array_test, ac.combine_integers(two_byte_int_arr, four_byte_int_arr))

    def test_decoder(self):
        newDecoder = MMTFDecoder()
        # Check that none of the getters are null
        newDecoder.decode_data(msgpack.unpackb(
            open("mmtf/tests/testdatastore/4CUP.mmtf").read()))


if __name__ == '__main__':
    unittest.main()
