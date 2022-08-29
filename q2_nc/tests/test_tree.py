from unittest import TestCase, main
import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()

from q2_nc._helpers import TreeClass

class TreeTests(TestCase):

    def setUp(self):
        #homo tree goes 9605->(1425170,9606->(63221,741158))
        #9605: 0
        #1425170: 1 
        #9606: 5
        #63221: 5
        #741158: 3

        self.df = pd.DataFrame([['h1', 9606, 'homo sapiens'],
                                    ['h2', 9606, 'homo sapiens'],
                                    ['h3', 9606, 'homo sapiens'],
                                    ['h4', 9606, 'homo sapiens'],
                                    ['h5', 9606, 'homo sapiens'],
                                    ['h6', 63221, 'homo sapiens Neandertal'],
                                    ['h7', 63221, 'homo sapiens Neandertal'],
                                    ['h8', 63221, 'homo sapiens Neandertal'],
                                    ['h9', 63221, 'homo sapiens Neandertal'],
                                    ['h10', 63221, 'homo sapiens Neandertal'],
                                    ['h11', 741158, 'homo sapiens Denisova'],
                                    ['h12', 741158, 'homo sapiens Denisova'],
                                    ['h13', 741158, 'homo sapiens Denisova'],
                                    ['h14', 1425170, 'homo heidelberg']],
                                    columns=['sample_id', 'ncbi_taxon_id', 'species'])


        homo_tree = 9605
        self.ncbi_tree = TreeClass(homo_tree, self.df, 'ncbi_taxon_id')
        

    def test_sum_look_up_taxid(self):
        real_sum = 14
        trial_sum = self.ncbi_tree.get_samples(self.ncbi_tree.get_root())
        self.assertEqual(real_sum, trial_sum)

    def test_node_get_node(self):
        real_sum = self.ncbi_tree.get_root()
        trial_sum = self.ncbi_tree.get_node(9605)
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
    
    def test_get_node_undefined(self):
        trial = self.ncbi_tree.get_node(1234)
        self.assertFalse(trial)


    def test_clade_set(self):
        #root = 9606
        root = self.ncbi_tree.get_node(9606)
        trial = self.ncbi_tree.make_clade_set(root)
        actual = set()
        actual.add(9606) 
        actual.add(63221)
        actual.add(741158)
        self.assertEqual(trial, actual)

    def test_bool_list(self):
        #root = 9606
        root = self.ncbi_tree.get_node(9606)
        trial = self.ncbi_tree.get_bool(root)
        inList = {9606, 63221, 741158}
        actual = self.df['ncbi_taxon_id'].isin(inList).astype(str)
        #9605: 0
        #1425170: 1 
        #9606: 5
        #63221: 5
        #741158: 3
        pd.testing.assert_series_equal(trial,actual)





if __name__ == '__main__':
    main()