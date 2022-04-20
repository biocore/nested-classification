import qiime2 
import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle

from sklearn import svm, datasets
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import roc_auc_score
from qiime2 import Artifact
from qiime2 import Visualization
from qiime2.plugins import sample_classifier
from qiime2.plugins import feature_table
#import mcdonald
import pandas as pd
from IPython.display import display

from ete3 import NCBITaxa
ncbi = NCBITaxa()


from treeClass import TreeClass
import qiime_code


class Train:

    
    def __init__(self, metadata, tax_col):
        self.metadata = metadata
        df = pd.read_csv(metadata, sep='\t')
        taxid = 7742 #vertebraes, we can change this
        self.ncbi_tree = TreeClass(taxid, df, tax_col)



#CHANGE 
df = pd.read_csv("metadata.tsv", sep='\t')
tax_col = "taxid_column" 
taxid = 7742 #vertebraes

tree = TreeClass(taxid, df, tax_col)

for node in tree.get_tree().traverse(strategy="levelorder"):
    taxid = node.taxid
    if tree.decision(taxid) is False:
        continue;
    for kids in node.get_children():
        taxid = kids.taxid
        
        if tree.decision(taxid):
            #here we have enough samples to train tree
            id_col = "sample_id" 
            boolIDS = tree.get_identifiers(taxid, id_col)
            df.insert(0, "IsChild", boolIDS, True)
            probs, estimator = trains ("metadata.tsv", "feature_table.")

