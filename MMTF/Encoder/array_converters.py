import struct
from MMTF.Common import Utils


def split_integers(int_array):
    small_array = []
    big_array = []
    # The first number is always in the big array
    big_array.append(int_array[0])
    counter = 0
    for in_int in int_array[1:]:
        if in_int >= Utils.MAX_SHORT:
            big_array.append(in_int)
            big_array.append(counter)
        else:
            small_array.append(in_int)
            counter+=1


def convert_ints_to_bytes(in_ints, num):
    out_str = ""
    for in_int in in_ints:
        out_str+=struct.pack(Utils.NUM_DICT[num],in_int)
    return out_str

def encode_chain_list(in_chains):
    out_s = ""
    for chain in in_chains:
        out_s += chain
        for i in range(Utils.CHAIN_LEN-len(chain)):
            out_s+=Utils.NULL_BYTE
    return out_s



def convert_floats_to_ints(in_ints, multiplier):
    out_floats = []
    for in_int in in_ints:
        out_floats.append(int(in_int * multiplier))
    return out_floats

def convert_chars_to_ints(in_chars):
    out_ints = []
    for in_char in in_chars:
        out_ints.append(int(in_char))
    return out_ints