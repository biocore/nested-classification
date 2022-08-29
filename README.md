# nested-classification

A QIIME 2 plugin for performing nested classification. This plugin utilizes the q2-sample-classifier: https://github.com/qiime2/q2-sample-classifier.git 

Nested-classification is a tool for comparing similarities of microbial data of humans to animals.

# Install

In a QIIME 2 enviroment: 
```
git fork https://github.com/biocore/nested-classification.git 
```
```
pip install -e .
```

# How to use

## 1. training-samples

The first method ran should be training-samples with animal (non-human) metadata and feature-table. 
This will train and output classifiers for later use. 

### Inputs 
1. QIIME 2 artifact feature-table
2. Corresponding non-human metadata including 'sample-id' as index column and 'ncbi-taxon-id' with information of host NCBI taxids
3. Pre-existing output directory (folder) for storing classifier models 
### Outputs
Output-directory folder will be populated with estimators labeled by their taxon IDs. 

## 2. predict-samples 

The second method queries human data against the previously trained models.

### Inputs
1. QIIME 2 **HUMAN** artifact feature-table 
2. The **same non-human** metadata used to train the stored models (this is used as a map)
3. An input-directory (folder) with the stored classifiers
### Outputs
1. probabilities.qzv: the probability of each query belonging to the taxid, or the model's predicted likelihood the individual is in the taxid's clade
2. predictions.qzv; predictions of "True" or "False" whether or not the individual belonds to that taxid's clade

# How does this work? 

q2-nc uses ete3.NBITaxa to pull information from NCBI Database. Using this, we are able to create a taxonomy tree from the taxids in the metadata. This taxonomy tree follows an evolutionary hierachy with vertebrate at the root and species as the leaves. Starting at vertebrate, we traverse down the tree to train models of subsets of the animal data at every (valid) node. Then, this same tree can be re-built so the human data can be inputted into the nested-classifiers through a depth traversal of the taxonomy tree. 

# References 
To be added..
QIIME2
q2-sample-classifier
ete3
