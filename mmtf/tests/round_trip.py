import unittest

import msgpack
import numpy

from mmtf import codecs,fetch,parse,parse_gzip, converters
from mmtf.api.default_api import ungzip_data
from mmtf.codecs import encoders
from mmtf.utils.codec_utils import parse_header
from mmtf.codecs.default_codec import codec_dict
from mmtf.codecs.decoders import numpy_decoders as decoders


class RoundTripTests(unittest.TestCase):

    def array_eq(self,array_one, array_two):
        import numpy as np
        if [x for x in np.isclose(array_one,array_two) if x]:
            return True
        else:
            try:
                if not array_one and not array_two:
                    return True
            except ValueError:
                pass
            print(array_one)
            print(array_two)
            print("Arrays not equal")
            return False

    def char_arr_eq(self,array_one, array_two):
        import numpy as np
        return np.array_equal(array_one,array_two)

    def iterate(self, data_one, data_two):
        chain_ind = 0
        group_ind = 0
        atom_ind_one = 0
        atom_ind_two = 0
        for model in data_one.chains_per_model:
            for chain in range(model):
                for group in range(data_one.groups_per_chain[chain_ind]):
                    self.char_arr_eq(data_one.group_list[data_one.group_type_list[group_ind]]["atomNameList"],
                                  data_two.group_list[data_two.group_type_list[group_ind]]["atomNameList"])
                    self.char_arr_eq(data_one.group_list[data_one.group_type_list[group_ind]]["elementList"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["elementList"])
                    self.array_eq(data_one.group_list[data_one.group_type_list[group_ind]]["bondOrderList"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["bondOrderList"])
                    self.array_eq(data_one.group_list[data_one.group_type_list[group_ind]]["bondAtomList"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["bondAtomList"])
                    self.array_eq(data_one.group_list[data_one.group_type_list[group_ind]]["formalChargeList"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["formalChargeList"])
                    self.assertEqual(data_one.group_list[data_one.group_type_list[group_ind]]["groupName"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["groupName"])
                    self.assertEqual(data_one.group_list[data_one.group_type_list[group_ind]]["singleLetterCode"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["singleLetterCode"])
                    self.assertEqual(data_one.group_list[data_one.group_type_list[group_ind]]["chemCompType"],
                                     data_two.group_list[data_two.group_type_list[group_ind]]["chemCompType"])
                    group_ind+=1
                chain_ind+=1
        return True

    def dict_list_equal(self,list_one,list_two):
        list_one = sorted(list_one, key=lambda x:sorted(x.keys()))
        list_two = sorted(list_two, key=lambda x:sorted(x.keys()))
        len_one = len(list_one)
        if len_one != len(list_two):
            self.assertTrue(False,"Lists of different lengths")
        for i in range(len_one):
            if list_one[i]!=list_two[i]:
                print(list_one[i])
                print(list_two[i])
            self.assertTrue(list_one[i]==list_two[i])

    def check_equal(self, data_one, data_two):
        self.assertTrue(self.array_eq(data_one.x_coord_list,data_two.x_coord_list))
        self.assertTrue(self.array_eq(data_one.y_coord_list,data_two.y_coord_list))
        self.assertTrue(self.array_eq(data_one.z_coord_list,data_two.z_coord_list))
        self.assertTrue(self.array_eq(data_one.b_factor_list,data_two.b_factor_list))
        self.assertTrue(self.array_eq(data_one.group_type_list,data_two.group_type_list))
        self.assertTrue(self.array_eq(data_one.occupancy_list,data_two.occupancy_list))
        self.assertTrue(self.array_eq(data_one.atom_id_list,data_two.atom_id_list))
        self.assertTrue(self.char_arr_eq(data_one.alt_loc_list,data_two.alt_loc_list))
        self.assertTrue(self.char_arr_eq(data_one.ins_code_list,data_two.ins_code_list))
        self.assertTrue(self.array_eq(data_one.group_id_list,data_two.group_id_list))
        self.dict_list_equal(data_one.entity_list,data_two.entity_list)
        self.dict_list_equal(data_one.bio_assembly,data_two.bio_assembly)
        self.dict_list_equal(data_one.group_list,data_two.group_list)
        self.assertTrue(self.array_eq(data_one.sequence_index_list,data_two.sequence_index_list))
        self.assertEqual(data_one.chains_per_model, data_two.chains_per_model)
        self.assertEqual(data_one.groups_per_chain, data_two.groups_per_chain)
        self.assertEqual(data_one.chain_name_list, data_two.chain_name_list)
        self.assertEqual(data_one.chain_id_list, data_two.chain_id_list)
        self.assertEqual(data_one.space_group,data_two.space_group)
        self.assertTrue(self.array_eq(data_one.bond_atom_list,data_two.bond_atom_list))
        self.assertTrue(self.array_eq(data_one.bond_order_list,data_two.bond_order_list))
        self.assertEqual(data_one.mmtf_version,data_two.mmtf_version)
        self.assertEqual(data_one.mmtf_producer,data_two.mmtf_producer)
        self.assertEqual(data_one.structure_id,data_two.structure_id)
        self.assertEqual(data_one.title,data_two.title)
        self.assertTrue(self.char_arr_eq(data_one.experimental_methods,data_two.experimental_methods))
        self.assertEqual(data_one.deposition_date,data_two.deposition_date)
        self.assertEqual(data_one.release_date,data_two.release_date)
        self.assertTrue(self.array_eq(data_one.sec_struct_list,data_two.sec_struct_list))
        self.assertEqual(data_one.r_free,data_two.r_free)
        self.assertEqual(data_one.r_work,data_two.r_work)
        self.assertEqual(data_one.resolution,data_two.resolution)
        self.assertEqual(data_one.unit_cell,data_two.unit_cell)
        self.assertEqual(data_one.num_bonds, data_two.num_bonds)
        self.assertEqual(data_one.num_chains, data_two.num_chains)
        self.assertEqual(data_one.num_models, data_two.num_models)
        self.assertEqual(data_one.num_atoms, data_two.num_atoms)
        self.assertEqual(data_one.num_groups, data_two.num_groups)
        self.assertTrue(self.iterate(data_one, data_two))


    def test_round_trip(self):
        data_in = parse_gzip("mmtf/tests/testdatastore/4CUP.mmtf.gz")
        data_in.write_file("test.mmtf")
        data_rt = parse("test.mmtf")
        self.check_equal(data_in, data_rt)

    def round_trip(self,pdb_id):
        data_in = fetch(pdb_id)
        data_in.write_file("test.mmtf")
        data_rt = parse("test.mmtf")
        self.check_equal(data_in, data_rt)

    def test_round_trip_list(self):
        id_list = [x.strip() for x in open("/Users/anthony/mmtf-python/all-pdb-list").readlines() if x ]
        other = open("other","w")
        io = open("io", "w")
        fail = open("fail", "w")
        for pdb_id in id_list:
            print(pdb_id)
            try:
                self.round_trip(pdb_id)
            except AssertionError:
                fail.write(pdb_id+"\n")
            except IOError:
                io.write(pdb_id+"\n")
            except:
                other.write(pdb_id+"\n")
        other.close()
        fail.close()
        io.close()

if __name__ == '__main__':
    unittest.main()
