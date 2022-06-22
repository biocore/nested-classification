from unittest import TestCase, main
import pandas as pd

from q2_nc.treeClass import TreeClass

class TreeTests(TestCase):

    def setUp(self):
        #homo tree goes 9605->(1425170,9606->(63221,741158))
        #9605: 0
        #1425170: 1 
        #9606: 5
        #63221: 5
        #741158: 3
        

        df = pd.read_csv('tests.tsv', sep='\t') 
        print(df)
        homo_tree = 9605
        self.ncbi_tree = TreeClass(homo_tree, df, 'ncbi_taxon_id')
        

    def test_sum_look_up_taxid(self):
        real_sum = 14
        trial_sum = self.ncbi_tree.look_up_taxid(9605)
        self.assertEqual(real_sum, trial_sum)

    def test_sum_look_up_taxid(self):
        real_sum = 14
        root_node = self.ncbi_tree.get_tree.get_tree_root()
        trial_sum = self.ncbi_tree.get_samples(root_node)
        self.assertEqual(real_sum, trial_sum)

    def test_taxids_per_sample(self):
        self.fail()

    def test_decision(self):
        self.assertFalse(self.ncbi_tree.decision(9605))
        


    #



if __name__ == '__main__':
    main()