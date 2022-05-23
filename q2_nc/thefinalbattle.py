
from tokenize import Triple
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
from os.path import exists

from treeClass import TreeClass
import qiime_code

import time

class Finale:

    def __init__(self, ft):
        self.ft = ft
        df = pd.read_csv("metadata_birdless.txt", sep='\t')
        #df.drop(df.index[(df["host_taxid"] == "not applicable")],axis=0,inplace=True)
        #df.drop(df.index[(df["host_taxid"] == "None")],axis=0,inplace=True)
        
        taxid = 7742
        tax_col = "ncbi_taxon_id"  
        #df[tax_col] = df[tax_col].astype(int)
        self.tree = TreeClass(taxid, df, tax_col)

    def root(self):
        return self.tree.get_tree().get_tree_root()

    def classify(self, taxid):
        feature_data = Artifact.load(self.ft)
        file = "estimator/" + str(taxid)+ ".qza"
        if not exists(file):
            print("bruh")
            print(taxid)
            avg_prob = 0
        else:
            esty = Artifact.load(file)
            y_pred, probs = sample_classifier.actions.predict_classification(feature_data, esty)
            avg_prob = self.probs_average(probs)
        return avg_prob
        #return y_pred, probs

    def probs_average(self, probs):
        prob = probs.view(pd.DataFrame)
        sum = prob["True"].sum()
        average = sum/len(prob)   
        return average 

    def checks(self, node):
        samples = self.tree.get_samples(node)
        if samples < 20:
            return True
        return False

    def not_unique(self, node, old_samples):
        samples = self.tree.get_samples(node)
        if old_samples == samples:
            return True
        return False


    def recursive(self, node):
        taxid = node.taxid

        if (node.is_leaf()):
            return taxid
        #TODO: change this to a list
        max_prob = 0
        max_node = NULL
        parent_samp = self.tree.get_samples(node)
        for child in node.get_children():
            child_taxid = child.taxid
            if self.checks(child):
                continue;

            #if a child is not unique, it's siblings have no samples 
            if self.not_unique(child, parent_samp):
                return self.recursive(child)

            avg = self.classify(child_taxid)
            if avg > max_prob:
                max_prob = avg
                max_node = child
            #if child_taxid == 40674:
             #   print(f"Mammals prob: {avg}")
            #    return self.recursive(child)
            #TODO: if else (equal) then add to list?? 
        if max_node == NULL:
            return taxid  
        #if max_prob < 0.8:
         #   return taxid  
        print(f"taxid: {max_node.taxid} | prob: {max_prob}")
        return self.recursive(max_node)





#ft = "man_127242_feature-table.qza"
ft = "ft2.0.qza"
#ft = "88201_feature-table.qza"
#og_df = pd.read_csv("metadata.tsv", sep='\t')
#tax_col = "ncbi_taxon_id" 
#id_col = "sample-id"

finishing_up = Finale(ft)
taxid = finishing_up.recursive(finishing_up.root())
#print(f"40674: {finishing_up.classify(40674)}")
print(f"final taxid: % {taxid}")
'''
print(f"8457: {finishing_up.classify(8457)}")
print(f"8492: {finishing_up.classify(8492)}")
print(f"32524: {finishing_up.classify(32524)}")
print(f"40674: {finishing_up.classify(40674)}")
print(f"314145: {finishing_up.classify(314145)}")
print(f"314146: {finishing_up.classify(314146)}")
print(f"1329799: {finishing_up.classify(1329799)}")
8457: 0.57
8492: 0.07
32524: 1.0
40674: 0.26
314145: 0.02
314146: 0.0
1329799: 0.2
8457 - Sauropsida
8492 - Archosauria
32524 - Amniota (yay)
40674 - Mammalia (sus)
314145 - placentals (bad)
314146 - Euarchontoglires (also placentals)
1329799 - Archelosauria (clade grouping turtles and archosaurs and their fossil relatives.)
'''





'''
df = pd.DataFrame()
df.insert(0, id_col, og_df[id_col], True)
df.insert(1, tax_col, og_df[tax_col], True)
#DF Has two columns: ids and taxids

taxid = 7742 #vertebraes
tree = TreeClass(taxid, df, tax_col)

node = tree.get_tree().get_tree_root()
#dont forget to change tacid to node.taxid
y_pred, probs = classify(ft, 9443)

pred = y_pred.view(pd.Series)
prob = probs.view(pd.DataFrame)

#print("pred:")
#print(pred.value_counts())
#print(pred[pred=="False"])

print("probs")
#print(prob)
#print(probs_average(probs))
#print(pred[~pred])
#print(pred)
#
'''
    

    



