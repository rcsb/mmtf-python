import struct

_NUM_DICT = {1:'b',2:'>h',4:'>i',8:'>q'}

def combine_integers(smallArray, bigArray):
    tot_count = len(bigArray)/2
    start = 0
    out_array = []
    for in_int in range(tot_count):
        out_array.append(bigArray[in_int*2])
        count = bigArray[in_int*2+1]
        for small_int in range(start, start+count):
            out_array.append(smallArray[small_int])
        start+=count
    return out_array




def convert_bytes_to_ints(in_bytes, num):
    outArr = []
    for i in range(len(in_bytes)/num):
        outArr.append(struct.unpack(_NUM_DICT[num],in_bytes[i*num:i*num+num])[0])
    return outArr

def decode_chain_list(in_bytes):
    tot_strings = len(in_bytes)/4
    out_strings = []
    for i in range(tot_strings):
        out_s = in_bytes[i*4:i*4+4].strip('\x00')
        out_strings.append(out_s)
    return out_strings


def convert_ints_to_floats(in_ints, divider):
    out_floats = []
    for in_int in in_ints:
        out_floats.append(in_int/divider)
    return out_floats

def convert_ints_to_chars(in_ints):
    out_chars = []
    for in_int in in_ints:
        out_chars.append(chr(in_int))
    return out_chars


