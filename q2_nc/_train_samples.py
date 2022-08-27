import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()

import biom
import qiime2
from qiime2 import Artifact
from qiime2 import Visualization
from qiime2.plugins import sample_classifier


from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import label_binarize

from _helpers import TreeClass


def _create_tree(meta, ft): 
	fet_tab = Artifact.load(ft)
	meta_d = qiime2.Metadata(meta)

	#fet_tab = qiime2.plugins.feature_table.methods(fet_tab, metadata=meta_d)
	tab = fet_tab.view(biom.Table)
	df = meta_d.to_dataframe()
	df = df.loc[tab.ids()]
	meta_d = qiime2.Metadata(df)
	
	return meta_d, fet_tab

def _ROC(probs, meta):
	data = probs.view(pd.DataFrame)
	
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
	train, test, trash_1, trash_2 = sample_classifier.actions.split_table(ft, meta.get_column("isChild"))
	estimator, importance = sample_classifier.actions.fit_classifier(train, meta.get_column("isChild"))
	y_pred, probs = sample_classifier.actions.predict_classification(test, estimator)
	roc = _ROC(probs, df) 
	return roc, estimator 


def train_samples(metadata_file: qiime2.Metadata, output_folder: str, ft_file: biom.Table, tax_col: str = 'ncbi_taxon_id', id_col: str = 'sample_name'):

    initial_df = pd.read_csv(metadata_file, sep='\t')

    new_df = pd.DataFrame()
    new_df.insert(0, id_col, initial_df[id_col], True)
    new_df.insert(1, tax_col, initial_df[tax_col], True)

    taxid = 7742
    tree = TreeClass(taxid, new_df, tax_col)


    subset = tree.make_clade_set(tree.get_root())
    for node in tree.get_tree().traverse(strategy="preorder"):
        taxid = node.taxid
        samples = tree.get_samples(node)
        curr_subset = tree.make_clade_set(node)
        #condition 1: at least 20 overall samples 
        if samples < 20:
            continue;
        #condition 2: sample set is unqiue 
        if subset == curr_subset:
            #estimator.save(path+str(taxid)+'.qza')
            continue
        boolIDS = tree.get_bool(taxid)
        # change create tree to return meta and ft
        #df = dataframe of metadata
        meta_df = new_df.copy()
        meta_df.insert(1, "isChild", boolIDS, True)
        meta_df.set_index(meta_df.columns[0], drop=True, append=False, inplace=True)

        #TODO: GET VISUALIZERS 
        meta, ft = _create_tree(meta_df, ft_file)
        roc_auc, estimator = _trains(meta, ft, meta_df) 

        if len(roc_auc) < 2:
            continue;

        estimator.save(output_folder+str(taxid)+'.qza')
    
            
    









