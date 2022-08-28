import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import qiime2
import biom
from q2_sample_classifier._type import (SampleEstimator, Classifier)


from q2_nc._helpers import TreeClass
import q2_nc._helpers2 



def training_samples(metadata: qiime2.Metadata, output_directory: str, table: biom.Table) -> (SampleEstimator[Classifier]):
    #default, make changeable? 
    tax_col = 'ncbi_taxon_id'
    id_col = 'sample_name'

    initial_df = pd.read_csv(metadata, sep='\t')

    new_df = pd.DataFrame()
    new_df.insert(0, id_col, initial_df[id_col], True)
    new_df.insert(1, tax_col, initial_df[tax_col], True)

    taxid = 7742
    tree = TreeClass(taxid, new_df, tax_col)
    sample_estimators = list()


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
        meta, ft = q2_nc._helpers2._create_tree(meta_df, table)
        roc_auc, estimator = q2_nc._helpers2._trains(meta, ft, meta_df)
        #estimator, importance, pred, summary, accuracy, probs =classify.classify_samples(,table,meta_df) 
        

        if len(roc_auc) < 2:
            continue;

        sample_estimators.append(estimator)
        #estimator.save(output_directory+str(taxid)+'.qza')
    return sample_estimators
            
    









