import biom
import qiime2
from qiime2 import Artifact
from qiime2 import Visualization
from q2_sample_classifier import classify
import pandas as pd 


from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize

def _create_tree(meta, table): 
	#fet_tab = Artifact.load(ft)
	#fet_tab = ft
	metadata = qiime2.Metadata(meta)
	metadata = metadata.filter_ids(table.ids(axis='sample'))
	
	table = table.filter(metadata.ids)

	#fet_tab = qiime2.plugins.feature_table.methods(fet_tab, metadata=meta_d)
	#tab = fet_tab.view(biom.Table)
	#df = meta_d.to_dataframe()
	#df = df.loc[tab.ids()]
	#meta_d = qiime2.Metadata(df)
	
	return metadata, table

def _ROC(probs, meta):
	#data = probs.view(pd.DataFrame)
	data = probs
	
	column = meta["isChild"]
	column_label = data.index
	
	column = column.loc[column_label] 
	labels = data.columns.values.tolist()
	labels.append("ignore")

	out = label_binarize(y=column, classes=labels)
	roc_auc = dict()
	fpr = dict()
	tpr = dict()
	data_num = data.to_numpy()

	for i in range(len(data_num[0])):
		fpr[i], tpr[i], _ = roc_curve(out[:,i], data_num[:,i])
		roc_auc[i] = auc(fpr[i],tpr[i])
	return roc_auc

def _trains(meta, ft, df): #return trained model
	train, test, trash_1, trash_2 = classify.split_table(ft, meta.get_column("isChild"))
	estimator, importance = classify.fit_classifier(train, meta.get_column("isChild"))
	y_pred, probs = classify.predict_classification(test, estimator)
	roc = _ROC(probs, df) 
	return roc, estimator 
