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
3. Train the estimators: python the_end_game.py
```

# How to run model:

```
1. Download human feature table from QIITA 
2. Update feature table variable with human samples file and update metadata variable with above trained animal file in "thefinalbattle.py"
3. Run the model: python thefinalbattle.py
```

