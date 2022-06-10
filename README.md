# nested-classification

A QIIME 2 plugin for performing nested classification

# Install

```
pip install -e .
```


# How to train estimators: 

```
1. Download animal metadata and feature table from QIITA
2. Update metadata and feature table variables in "the_end_game.py" with the downloaded files 
3. Train the estimators (classifiers): python the_end_game.py
```
the_end_game.py uses qiimecode.py to train individual models and treeClass.py to map the taxon-ids and number of samples in the metadata to the trained estimators. 

# How to run model:

```
1. Download human feature table from QIITA 
2. Update feature table variable with human samples file and update metadata variable with above trained animal file in "thefinalbattle.py"
3. Run the model: python thefinalbattle.py
```
thefinalbattle.py uses treeClass.py to map the trained estimators to a hierachical, taxonomic ranking such that Qiime2 can output the highest probality taxon-id, or taxa, per sibling nodes in the tree. 
