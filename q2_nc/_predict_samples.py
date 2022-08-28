import typing
import qiime2
import biom
from qiime2 import Artifact
from qiime2.plugins import sample_classifier
from q2_types.sample_data import SampleData
from q2_sample_classifier._type import (ClassifierPredictions, Probabilities)
from _helpers import TreeClass
import pandas as pd
from ete3 import NCBITaxa
from os.path import exists
ncbi = NCBITaxa()




def _recursive(tree, node, probalities: pd.DataFrame, predictions: pd.Series, ft, path):
        taxid = node.taxid
        if (node.is_leaf()):
            return probalities, predictions
        
        max_prob = 0
        max_node = None
        parent_samp = tree.get_samples(node)
        parent_clade = tree.make_clade_set(node)
        for child in node.get_children():
            child_taxid = child.taxid
            child_clade = tree.make_clade_set(child)

            child_samples = tree.get_samples(child)
            if child_samples < 20:
                continue
            #if a child is not unique, it's siblings have no samples 
            if parent_clade == child_clade:
                return _recursive(tree, child, probalities, predictions, ft, path)

            #avg = self.classify(child_taxid):
            feature_data = Artifact.load(ft)
            file = path + str(child_taxid)+ ".qza"

            
            if not exists(file):
                avg_prob = 0
                print(f'Warning: {file} not found. Potential metadata issue.')
            else:
                estimator = Artifact.load(file)
                y_pred, probs = sample_classifier.actions.predict_classification(feature_data, estimator)
                probalities.append(probs)
                predictions.append(y_pred)
                avg = probs.view(pd.DataFrame)['True'].mean()               
            if avg > max_prob:
                max_prob = avg
                max_node = child
                
        if max_node == None:
            return probalities, predictions

        return _recursive(tree, max_node, probalities, predictions, ft, path)


def predict_samples(
        metadata: qiime2.Metadata, 
        table: biom.Table, 
        input_directory: str) -> pd.DataFrame:
    tax_col = 'ncbi_taxon_id'
    df = pd.read_csv(metadata, sep='\t')
    path = input_directory
    taxid = 7742

    tree = TreeClass(taxid, df, tax_col)

    node = tree.get_root()

    probs = pd.DataFrame()
    pred = pd.Series()
    probabilites, predictions = _recursive(tree, node, probs, pred, table, path)
    return probabilites


