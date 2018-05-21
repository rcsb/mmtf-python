[![Build Status](https://travis-ci.org/rcsb/mmtf-python.svg?branch=master)](https://travis-ci.org/rcsb/mmtf-python)
[![Code Health](https://landscape.io/github/rcsb/mmtf-python/master/landscape.svg?style=flat)](https://landscape.io/github/rcsb/mmtf-python/master)
[![Version](http://img.shields.io/badge/version-1.1.2-blue.svg?style=flat)](https://github.com/rcsb/mmtf-python/)
[![License](http://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat)](https://github.com/rcsb/mmtf-python/blob/master/LICENSE.txt)
[![Changelog](https://img.shields.io/badge/changelog--lightgrey.svg?style=flat)](https://github.com/rcsb/mmtf-python/blob/master/CHANGELOG.md)


The **m**acro**m**olecular **t**ransmission **f**ormat (MMTF) is a binary encoding of biological structures.

This repository holds the Python 2 and 3 compatible API, encoding and decoding libraries. 

The MMTF python API is available from pip:
```
pip install mmtf-python
```

Quick getting started.

1) Get the data for a PDB structure and print the number of chains:
```python
from mmtf import fetch
# Get the data for 4CUP
decoded_data = fetch("4CUP")
print("PDB Code: "+str(decoded_data.structure_id)+" has "+str(decoded_data.num_chains)+" chains")
```
2) Show the charge information for the first group:
```python
print("Group name: "+str(decoded_data.group_list[0]["groupName"])+" has the following atomic charges: "+",".join([str(x) for x in decoded_data.group_list[0]["formalChargeList"]]))

```
3) Show how many bioassemblies it has:
```python
print("PDB Code: "+str(decoded_data.structure_id)+" has "+str(len(decoded_data.bio_assembly))+" bioassemblies")
```
