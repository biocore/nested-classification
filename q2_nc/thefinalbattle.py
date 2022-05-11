
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
        df = pd.read_csv("metadata.tsv", sep='\t')
        taxid = 7742
        tax_col = "ncbi_taxon_id" 
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

    #find unique child -> return node
    '''
    def unique_child(self, node):
        valid = True
        if (child.is_leaf()):
            valid = False
            return node, valid
        max_taxid = NULL
        max_prob = 0
        samples = self.tree.get_samples(node)
        for child in node.get_children():
    	    if self.checks(child):
    		    continue
            
            if self.not_unique(child, samples):
                child, valid = self.unique_child(child)
            else: 
                return self.recursive(node)

        return max_taxid, valid
        '''


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

            #TODO
            if self.not_unique(child, parent_samp):
                return self.recursive(child)
                #child, test = self.unique_child(node)

            avg = self.classify(child_taxid)
            if avg >= max_prob:
                max_prob = avg
                max_node = child
        if max_node == NULL:
            return taxid  
        #if max_prob < 0.5:
         #   return max_node.taxid  
        return self.recursive(max_node)


'''
feature table, node, meta data  

def classify(ft, taxid_node):
	master_store = {}
	file = "estimator/" + str(taxid_node.taxid)+ ".qza"
	esty = Artifact.load(file)
	y_pred, probs = sample_classifier.actions.predict_classification(feature_data, esty)
        
    #goal: if leaf -> 
	if taxid_node.isLeaf() == false:
		max
		max_taxid
		for i in probs:
		if probs.val < max:
			max_taxid = probs.taxid
		max_taxid1 = classify(ft, max_taxid)
	else:
		return (max_taxid = max_taxid1)

        master_store = master_store | traverse(ft , taxid_node) #merging the returned dictionary with the returned dictionary should work for python 3.9 and up
	closest_match = max(master_store, key = master_store.get) # should return the key of the max value in this case the highest ROC  
	
	return y_pred, probs

def traverse(ft, taxid_node)
	store = {}# a dictionary that store the leafs that have greater then 0.5
	for curr_node in taxid_node.traverse(strategy="preorder"):
		y_pred, probs = sample_classifier.actions.predict_classification(feature_data, esty):
			if(ROC(probs, get_bool(taxid)) > 0.5): 
				if(node.is_leaf()):
					store[taxid] =  ROC(probs, get_bool(taxid))

	return store 

def caller(ft, root, meta):
	feature_data = Artifact.load(ft)
	classify(feature_data,taxid_node)


'''


#ft = "man_127242_feature-table.qza"
ft = "ft2.0.qza"
og_df = pd.read_csv("metadata.tsv", sep='\t')
tax_col = "ncbi_taxon_id" 
id_col = "sample-id"

finishing_up = Finale(ft)
taxid = finishing_up.recursive(finishing_up.root())
print(taxid)
print(finishing_up.classify(taxid))


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
#printthis = Artifact.view(y_pred, str)
#pred = Visualization.load(probs) 
#pred = 




while node is not NULL: 
    taxid = node.taxid
    newSamples = tree.get_samples(node)
    if newSamples < 20:
        continue;
    if samples == newSamples:
        continue
    samples = newSamples
'''
    

    



