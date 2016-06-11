from __future__ import division
import struct
import mmtf
import math

def convert_bytes_to_ints(in_bytes, num):
    """Convert a byte array into an integer arrays. The number of bytes forming an integer
    is defined by num
    :param the input bytes
    :param the number of bytes per int
    :return the integer array"""
    out_arr = []
    for i in range(len(in_bytes)//num):
        val = in_bytes[i * num:i * num + num]
        unpacked = struct.unpack(mmtf.NUM_DICT[num], val)
        out_arr.append(unpacked[0])
    return out_arr

def decode_chain_list(in_bytes):
    """Convert a list of bytes to a list of strings. Each string is of length
    mmtf.CHAIN_LEN
    :param the input bytes
    :return the decoded list of strings"""
    tot_strings = len(in_bytes) // mmtf.CHAIN_LEN
    out_strings = []
    for i in range(tot_strings):
        out_s = in_bytes[i * mmtf.CHAIN_LEN:i * mmtf.CHAIN_LEN + mmtf.CHAIN_LEN]
        out_strings.append(out_s.decode("utf-8").strip(mmtf.NULL_BYTE))
    return out_strings

def convert_ints_to_floats(in_ints, divider):
    """Conver integers to floats by division.
    :param the integer array
    :param the divider
    :return the array of floats produced"""
    out_floats = []
    for in_int in in_ints:
        out_floats.append(in_int/divider)
    return out_floats

def convert_ints_to_chars(in_ints):
    """Convert integers to chars.
    :param the input integers
    :return the character array converted"""
    out_chars = []
    for in_int in in_ints:
        out_chars.append(chr(in_int))
    return out_chars

def recursive_index_encode(int_array, max=32767, min=-32768):
    """Pack an integer array using recursive indexing
    :param int_array the input array of integers
    :param max the maximum integer size
    :param min the minimum integer size
    :return the array of integers after recursive index encoding"""
    out_arr = []
    for curr in int_array:
        if curr >= 0 :
            while curr >= max:
                out_arr.append(max)
                curr -=  max
        else:
            while curr <= min:
                out_arr.append(min)
                curr += math.fabs(min)
        out_arr.append(curr)
    return out_arr


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

def convert_ints_to_bytes(in_ints, num):
    """Convert an array of integers to a byte array using the num parameter
    to specify the number of bytes per int.
    :param in_ints the input array of integers
    :param num the number of bytes per integer
    :return the encoded array"""
    out_str = ""
    for in_int in in_ints:
        out_str+=struct.pack(mmtf.NUM_DICT[num], in_int)
    return out_str


def encode_chain_list(in_chains):
    """Convert a list of strings to bytes of a set length.
    :param in_chains the input list of strings
    :return the byte array of the encoded string"""
    out_s = ""
    for chain in in_chains:
        out_s += chain
        for i in range(mmtf.CHAIN_LEN-len(chain)):
            out_s+= mmtf.NULL_BYTE
    return out_s


def convert_floats_to_ints(in_floats, multiplier):
    """Convert floating points to integers using a multiplier.
    :param in_floats the input floats
    :param multiplier the multiplier to be used for conversion. Corresponds to the precisison.
    :return the array of integers encoded"""
    out_ints = []
    for in_float in in_floats:
        out_ints.append(int(in_float * multiplier))
    return out_ints


def convert_chars_to_ints(in_chars):
    """Convert an array of chars to an array of ints.
    :param in_chars the input characters
    :return the array of integers"""
    out_ints = []
    for in_char in in_chars:
        out_ints.append(int(in_char))
    return out_ints