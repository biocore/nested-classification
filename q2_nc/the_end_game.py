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


#class Train:

    
#    def __init__(self, metadata, tax_col):
#        self.metadata = metadata
 #       df = pd.read_csv(metadata, sep='\t')
 #       taxid = 7742 #vertebraes, we can change this
  #      self.ncbi_tree = TreeClass(taxid, df, tax_col)




df = pd.read_csv("metadata.tsv", sep='\t')
tax_col = "ncbi_taxon_id" 
taxid = 7742 #vertebraes
path = "estimator/"
#os.mkdir(path, mode = 0o777, dir_fd = None)
tree = TreeClass(taxid, df, tax_col)

for node in tree.get_tree().traverse(strategy="preorder"):
    taxid = node.taxid
    #Joelle speed decistion 
    #if tree.decision(taxid) is False:
    #    continue; 
    #else:
        #here we have enough samples to train tree
    #id_col = "sample_id" 
    boolIDS = tree.get_bool(taxid)
    print(boolIDS)
    # change create tree to return meta and ft
    #df = dataframe of metadata
    meta_df = df
    meta_df.insert(1, "isChild", boolIDS, True)
    #THIS LINE DOES NOT WORK:
    meta_df.set_index(meta_df.columns[0], drop=True, append=False, inplace=True)
    print(meta_df)
    meta, ft = qiime_code.create_tree(meta_df,'tb.qza')
    #meta.insert(0, "isChild", boolIDS, True)
    # change trains to return roc_auc instead of probs
    roc_auc, estimator = qiime_code.trains(meta, ft) # only estimator is valuable, classifier
    # can we save in the node?
    if roc_auc[1] > .5: 
        #path_list=path.split"/"
        #i =0
        #i =0
        #while(!taxid.isChild(path_list[i]):
            #i++
        #for j in path_list[0:i+1]
           #path = path + '/' + j   
        #path = path+taxid
       
        estimator.save('path'+taxid+'qza')
           
        # estimator > output @ row_taxid
        #kids.estimator = estimator
