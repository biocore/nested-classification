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

import os

from treeClass import TreeClass
import qiime_code

import time


#class Train:

    
#    def __init__(self, metadata, tax_col):
#        self.metadata = metadata
 #       df = pd.read_csv(metadata, sep='\t')
 #       taxid = 7742 #vertebraes, we can change this
  #      self.ncbi_tree = TreeClass(taxid, df, tax_col)



count = 0
og_df = pd.read_csv("metadata.tsv", sep='\t')
tax_col = "ncbi_taxon_id" 
id_col = "sample-id"

df = pd.DataFrame()
df.insert(0, id_col, og_df[id_col], True)
df.insert(1, tax_col, og_df[tax_col], True)

taxid = 7742 #vertebraes
path = "estimator/"
#os.mkdir(path, mode = 0o777, dir_fd = None)
tree = TreeClass(taxid, df, tax_col)

#tree.print_total_samples()
samples = 0
initial = time.perf_counter()
for node in tree.get_tree().traverse(strategy="preorder"):
    
    taxid = node.taxid
    newSamples = tree.get_samples(node)
    #condition 1: at least 20 overall samples 
    if newSamples < 20:
        #final = time.perf_counter()
        #print(final-initial)
        continue;
    #condition 2: sample set is unqiue 
    if samples == newSamples:
        #estimator.save(path+str(taxid)+'.qza')
        #final = time.perf_counter()
        #print(final-initial)
        continue
    samples = newSamples
    
    #Joelle speed decistion 
    #if tree.decision(taxid) is False:
    #    continue; 
    #else:
        #here we have enough samples to train tree
    #id_col = "sample_id" 
    boolIDS = tree.get_bool(taxid)
    #print(boolIDS)
    # change create tree to return meta and ft
    #df = dataframe of metadata
    meta_df = df.copy()
    meta_df.insert(1, "isChild", boolIDS, True)
    #THIS LINE DOES NOT WORK:
    meta_df.set_index(meta_df.columns[0], drop=True, append=False, inplace=True)
    
    #print(meta_df)
    try:
        meta, ft = qiime_code.create_tree(meta_df,'tb.qza')
    except:
        print("*** ERROR *** ERROR *** ERROR *** ERROR ***")
        print(taxid)
        print("some error in create_tree")
        continue;
    #meta.insert(0, "isChild", boolIDS, True)
    # change trains to return roc_auc instead of probs
    try:
        roc_auc, estimator = qiime_code.trains(meta, ft, meta_df) # only estimator is valuable, classifier
    except:
        print("*** ERROR *** ERROR *** ERROR *** ERROR ***")
        print(taxid)
        print("some error in trains")
        continue;
    
    if len(roc_auc) < 2:
        #tree.prune(node.get_children())
        continue;
    # can we save in the node?
    #estimator.save(path+str(taxid)+'.qza')
    if roc_auc[1] > 0.5: 
        #path_list=path.split"/"
        #i =0
        #i =0
        #while(!taxid.isChild(path_list[i]):
            #i++
        #for j in path_list[0:i+1]
           #path = path + '/' + j   
        #path = path+taxid
        count+=1
        estimator.save(path+str(taxid)+'.qza')
        #final = time.perf_counter()
        # estimator > output @ row_taxid
        #kids.estimator = estimator
    #print(final-initial)
    
final = time.perf_counter()
print(count)
print("\n")
print(final-initial)