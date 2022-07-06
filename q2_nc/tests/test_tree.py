from unittest import TestCase, main
import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()

from q2_nc.treeClass import TreeClass

class TreeTests(TestCase):

    def setUp(self):
        #homo tree goes 9605->(1425170,9606->(63221,741158))
        #9605: 0
        #1425170: 1 
        #9606: 5
        #63221: 5
        #741158: 3
        

        self.df = pd.read_csv('tests/tests.tsv', sep='\t') 
        homo_tree = 9605
        self.ncbi_tree = TreeClass(homo_tree, self.df, 'ncbi_taxon_id')
        

    def test_sum_look_up_taxid(self):
        real_sum = 14
        trial_sum = self.ncbi_tree.look_up_taxid(9605)
        self.assertEqual(real_sum, trial_sum)

    def test_node_look_up_taxid(self):
        real_sum = self.ncbi_tree.get_root()
        trial_sum = self.ncbi_tree.look_up_taxid(9605, False)
        self.assertEqual(real_sum, trial_sum)    

    def test_sum_get_samples(self):
        real_sum = 14
        root_node = self.ncbi_tree.get_tree().get_tree_root()
        trial_sum = self.ncbi_tree.get_samples(root_node)
        self.assertEqual(real_sum, trial_sum)


    def test_get_samples_undefined(self):   
        actual = -1
        trial = self.ncbi_tree.get_samples(1234)
        self.assertEqual(trial, actual)
    


    def test_clade_set(self):
        trial = self.ncbi_tree.make_clade_set(9606)
        actual = set()
        actual.add(9606) 
        actual.add(63221)
        actual.add(741158)
        self.assertEqual(trial, actual)

    def test_bool_list(self):
        trial = self.ncbi_tree.get_bool(9606)
        inList = {9606, 63221, 741158}
        actual = self.df['ncbi_taxon_id'].isin(inList).astype(str)
        #9605: 0
        #1425170: 1 
        #9606: 5
        #63221: 5
        #741158: 3
        pd.testing.assert_series_equal(trial,actual)





    

    #def test_taxids_per_sample(self):
    #    self.fail()

    #def test_decision(self):
    #    self.assertFalse(self.ncbi_tree.decision(9605))
        


    #



if __name__ == '__main__':
    main()