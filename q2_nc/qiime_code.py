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

meta_d = None
fet_tab = None	
	
def create_tree(meta, ft): 
	fet_tab = Artifact.load(ft)
	meta_d = qiime2.Metadata(meta)
	return meta_d, fet_tab
	
	

def divisor(meta):
 probs, estimator = trains(meta) 
	  

def store():
	return None 

#create_tree('mcdonald/mds.tsv','mcdonald/tb.qza')

def trains(meta, ft, df): #return trained model
	type(fet_tab)
	train, test, trash_1, trash_2 = sample_classifier.actions.split_table(ft, meta.get_column("isChild"))
	estimator, importance = sample_classifier.actions.fit_classifier(train, meta.get_column("isChild"))
	y_pred, probs = sample_classifier.actions.predict_classification(test, estimator)
	#ROC(probs, df) 
	return probs, estimator 

def ROC(probs, meta):
	data = probs.view(pd.DataFrame)
	#meta = pd.read_csv('metadata.tsv', sep = '\t')
	#meta.set_index("sample-id", inplace = True)
	column = meta["isChild"]
	column_label = data.index
	print(column_label)
	#the meta data that data doesn't 
	column = column.loc[column_label] 
	#listy = column.tolist()
	labels = data.columns.values.tolist()
	print(labels)
	#l = len(labels)
	#w = len(column)
	out = label_binarize(column, labels)
	#print(type(out))
	roc_auc = dict()
	fpr = dict()
	tpr = dict()
	type(out)
	data_num = data.to_numpy()
	for i in range(len(labels)):
		#print(out[:,i])
		#print(data.to_numpy()[:,i])
		fpr[i], tpr[i], _ = roc_curve(out[:,i], data_num[:,i])
		roc_auc[i]=auc(fpr[i],tpr[i])
		print(roc_auc[i])
	return roc_auc

 
#def main(met, ft):
#	meta_d, fet_tab = create_tree(met,ft)
#	probs, estimator = trains(meta_d,fet_tab)


#main('metadata.tsv','tb.qza')

