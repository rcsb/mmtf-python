[![Build Status](https://travis-ci.org/rcsb/mmtf-python.svg?branch=master)](https://travis-ci.org/rcsb/mmtf-python)
[![Code Health](https://landscape.io/github/rcsb/mmtf-python/master/landscape.svg?style=flat)](https://landscape.io/github/rcsb/mmtf-python/master)
[![Status](http://img.shields.io/badge/status-experimental-red.svg?style=flat)](https://github.com/rcsb/mmtf-python/)

# mmtf-python

The macromolecular transmission format (MMTF) is a binary encoding of biological structures.

This repository holds the Python API, encoding and decoding libraries. 

The alpha release is available from pip:
```
pip install mmtf-python
```

Quick getting started.

1) Get the data for a PDB structure and print the number of chains:
``` #python
 from MMTF.Decoder.reader_utils import get_decoded_data_from_url
 # Get the data for 4CUP
 decoded_data = get_decoded_data_from_url("4CUP")
 print "PDB Code: "+decoded_data.get_structure_id()+" has "+str(decoded_data.get_num_chains())+" chains"
```
2) Show the charge information for the first group:
```
 print "Group name: "+decoded_data.get_group_name(0)+" has the following atomic charges: "+",".join([str(x) for x in decoded_data.get_group_atom_charges(0)])

```
3) Show how many bioassemblies it has:
```
print "PDB Code: "+decoded_data.get_structure_id()+" has "+decoded_data.get_num_bioassemblies()+" bioassemblies");
```
