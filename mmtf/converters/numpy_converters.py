from __future__ import division
import numpy
import mmtf


def convert_bytes_to_ints(in_bytes, num):
    """Convert a byte array into an integer array. The number of bytes forming an integer
    is defined by num
    :param the input bytes
    :param the number of bytes per int
    :return the integer array"""
    dt = numpy.dtype('>i' + str(num))
    return numpy.frombuffer(in_bytes, dt)

def decode_chain_list(in_bytes):
    """Convert a list of bytes to a list of strings. Each string is of length
    mmtf.CHAIN_LEN
    :param the input bytes
    :return the decoded list of strings"""
    bstrings = numpy.frombuffer(in_bytes, numpy.dtype('S' + str(mmtf.CHAIN_LEN)))
    return [s.decode("ascii").strip(mmtf.NULL_BYTE) for s in bstrings]

def convert_ints_to_floats(in_ints, divider):
    """Conver integers to floats by division.
    :param the integer array
    :param the divider
    :return the array of floats produced"""
    return (numpy.asfarray(in_ints) / divider)

def recursive_index_decode(int_array, max=32767, min=-32768):
    """Unpack an array of integers using recursive indexing.
    :param int_array the input array of integers
    :param max the maximum integer size
    :param min the minimum integer size
    :return the array of integers after recursive index decoding"""
    out_arr = []
    encoded_ind = 0
    while encoded_ind < len(int_array):
        decoded_val = 0
        while int_array[encoded_ind]==max or int_array[encoded_ind]==min:
            decoded_val += int_array[encoded_ind]
            encoded_ind+=1
            if int_array[encoded_ind]==0:
                break
        decoded_val += int_array[encoded_ind]
        encoded_ind+=1
        out_arr.append(decoded_val)
    return out_arr