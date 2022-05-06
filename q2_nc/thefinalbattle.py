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
from zmq import NULL
ncbi = NCBITaxa()

import os

from treeClass import TreeClass
import qiime_code

import time



def classify(ft, taxid):
    feature_data = Artifact.load(ft)
    file = "estimator/" + str(taxid)+ ".qza"
    esty = Artifact.load(file)
    y_pred, probs = sample_classifier.actions.predict_classification(feature_data, esty)

    return y_pred, probs

def traverse(probs, meta, taxid_node)
    result = ROC(probs, meta)
    if (result>0.5):
         children = taxid_node.get_children()
         children.total_samples()
         #tranform metat 
            #call with childrens meta data 
    
  

ft = "tb.qza"
og_df = pd.read_csv("metadata.tsv", sep='\t')
tax_col = "ncbi_taxon_id" 
id_col = "sample-id"

df = pd.DataFrame()
df.insert(0, id_col, og_df[id_col], True)
df.insert(1, tax_col, og_df[tax_col], True)
#DF Has two columns: ids and taxids

taxid = 7742 #vertebraes
tree = TreeClass(taxid, df, tax_col)

node = tree.get_tree().get_tree_root()
y_pred, probs = classify(ft, node.taxid)

#pred = Visualization.load(y_pred)
print(type(y_pred))
print(y_pred[0])
#pred = y_pred.view(pd.DataFrame)
#print(pred)
#printthis = Artifact.view(y_pred, str)



'''
while node is not NULL: 
    taxid = node.taxid
    newSamples = tree.get_samples(node)
    if newSamples < 20:
        continue;
    if samples == newSamples:
        continue
    samples = newSamples
'''
    

    



