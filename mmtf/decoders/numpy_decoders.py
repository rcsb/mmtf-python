import numpy

def delta_decode(in_array):
    """A function to delta decode an int array
    :param the input array of integers
    :return the decoded array"""
    in_array = numpy.asarray(in_array)
    return in_array.cumsum()