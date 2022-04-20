from unittest import TestCase, main
import pandas as pd

from q2_nc.treeClass import TreeClass

class TreeTests(TestCase):

    def setUp(self):
        df = pd.read_csv('tests.tsv', sep='\t') 
        homo_tree = "homo"
        self.ncbi_tree = TreeClass(homo_tree, df, 'ncbi_taxon_id')
        self.ncbi_tree.build_sample_tree()


    
    #build tree correctly
    def test_print_all_samples(self):
        self.fail()

    def test_total_samples(self):
        self.fail()

    def test_taxids_per_sample(self):
        self.fail()

    def test_decision(self):
        self.assertFalse(self.ncbi_tree.decision(9605))
        


    #



if __name__ == '__main__':
    main()