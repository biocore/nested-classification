from unittest import TestCase, main
import pandas as pd
import pandas.testing as pdt

from q2_nc._training_nested import training_samples
from q2_nc._helpers import TreeClass




class ClassifierTests(TestCase):

    def setUp(self):
        df = pd.read_csv('metadata_test.tsv', sep='\t')
        tax_col = 'ncbi_taxon_id'
        id_col = 'sample_name'
        taxid = 7742
        tree = TreeClass(taxid, df, tax_col)



    def test_run_random_forests(self):
        # take pandas series describing binary labels for samples
        # take a feature table
        # construct a classifier
        # return measures indicating the performance of the classifier
        self.fail()

    def test_append_to_results_hierarchy(self):
        # take classification performance results
        # label the results by the ncbi taxonomy id describing the clade
        # add them to a node in our results hierarchy
        self.fail()

    def test_save_results_hierarchy(self):
        # do smart stuff
        self.fail()


if __name__ == '__main__':
    main()
