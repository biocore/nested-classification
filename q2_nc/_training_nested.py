import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import qiime2
import biom
from q2_sample_classifier._type import (SampleEstimator, Classifier)
import pickle
from sklearn.pipeline import Pipeline


from q2_nc._helpers import TreeClass
import q2_nc._helpers2 



def training_samples(metadata: qiime2.Metadata, output_directory: str, table: biom.Table) -> (Pipeline):
    #default, make changeable? 
    tax_col = 'ncbi_taxon_id'
    id_col = 'sample_name'

    initial_df = metadata.to_dataframe()
    print(initial_df)
    print(initial_df[tax_col])

    new_df = pd.DataFrame()
    new_df.insert(0, id_col, initial_df.index.values, True)
    new_df.insert(1, tax_col, initial_df[tax_col].values, True)
    taxid = 7742
    print(new_df)
    tree = TreeClass(taxid, new_df, tax_col)
    tree.print_total_samples
    sample_estimators = list()


    subset = set()
    print("before for-loop")
    for node in tree.get_tree().traverse(strategy="preorder"):
        taxid = node.taxid
        print(f"In for-loop for {taxid}")
        samples = tree.get_samples(node)
        curr_subset = tree.make_clade_set(node)
        #condition 1: at least 20 overall samples 
        if samples < 20:
            print(f"\t There are too little samples: {samples}")
            continue;
        #condition 2: sample set is unqiue 
        if subset == curr_subset:
            continue
        subset = curr_subset
        boolIDS = tree.get_bool(node)
        # change create tree to return meta and ft
        meta_df = new_df.copy()
        meta_df.insert(1, "isChild", boolIDS, True)
        meta_df.set_index(meta_df.columns[0], drop=True, append=False, inplace=True)

        #TODO: GET VISUALIZERS 
        print(f"{taxid}: for pre-training")
        meta, ft = q2_nc._helpers2._create_tree(meta_df, table)
        roc_auc, estimator = q2_nc._helpers2._trains(meta, ft, meta_df) 
        

        if len(roc_auc) < 2:
            continue;
        print(f"{taxid}: pre-saving")
        sample_estimators.append(estimator)
        filename = output_directory + "/" + str(taxid) + ".qza"
        outfile = open(filename, 'wb')
        pickle.dump(estimator, outfile)
        outfile.close()
        print(f"{taxid}: saved")
    
    print("Out of for-loop")
    return sample_estimators 
            
    









