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
### QIIME2:

Bolyen E, Rideout JR, Dillon MR, Bokulich NA, Abnet CC, Al-Ghalith GA, Alexander H, Alm EJ, Arumugam M, Asnicar F, Bai Y, Bisanz JE, Bittinger K, Brejnrod A, Brislawn CJ, Brown CT, Callahan BJ, Caraballo-Rodríguez AM, Chase J, Cope EK, Da Silva R, Diener C, Dorrestein PC, Douglas GM, Durall DM, Duvallet C, Edwardson CF, Ernst M, Estaki M, Fouquier J, Gauglitz JM, Gibbons SM, Gibson DL, Gonzalez A, Gorlick K, Guo J, Hillmann B, Holmes S, Holste H, Huttenhower C, Huttley GA, Janssen S, Jarmusch AK, Jiang L, Kaehler BD, Kang KB, Keefe CR, Keim P, Kelley ST, Knights D, Koester I, Kosciolek T, Kreps J, Langille MGI, Lee J, Ley R, Liu YX, Loftfield E, Lozupone C, Maher M, Marotz C, Martin BD, McDonald D, McIver LJ, Melnik AV, Metcalf JL, Morgan SC, Morton JT, Naimey AT, Navas-Molina JA, Nothias LF, Orchanian SB, Pearson T, Peoples SL, Petras D, Preuss ML, Pruesse E, Rasmussen LB, Rivers A, Robeson MS, Rosenthal P, Segata N, Shaffer M, Shiffer A, Sinha R, Song SJ, Spear JR, Swafford AD, Thompson LR, Torres PJ, Trinh P, Tripathi A, Turnbaugh PJ, Ul-Hasan S, van der Hooft JJJ, Vargas F, Vázquez-Baeza Y, Vogtmann E, von Hippel M, Walters W, Wan Y, Wang M, Warren J, Weber KC, Williamson CHD, Willis AD, Xu ZZ, Zaneveld JR, Zhang Y, Zhu Q, Knight R, and Caporaso JG. 2019. Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2. Nature Biotechnology 37: 852–857. https://doi.org/10.1038/s41587-019-0209-9


### q2-sample-classifier: 
@article {Bokulich306167,
  author = {Bokulich, Nicholas and Dillon, Matthew and Bolyen, Evan and Kaehler, Benjamin D and Huttley, Gavin A and Caporaso, J Gregory},
  title = {{q2-sample-classifier}: machine-learning tools for microbiome classification and regression},
  year = {2018},
  doi = {10.21105/joss.00934},
  journal = {Journal of Open Source Software},
  volume={3},
  number={30},
  pages={934}
}

@article{pedregosa2011scikit,
  title={Scikit-learn: Machine learning in Python},
  author={Pedregosa, Fabian and Varoquaux, Ga{\"e}l and Gramfort, Alexandre and Michel, Vincent and Thirion, Bertrand and Grisel, Olivier and Blondel, Mathieu and Prettenhofer, Peter and Weiss, Ron and Dubourg, Vincent and Vanderplas, Jake and Passos, Alexandre and Cournapeau, David and Brucher, Matthieu and Perrot, Matthieu and Duchesnay, {\'E}douard},
  journal={Journal of machine learning research},
  volume={12},
  number={Oct},
  pages={2825--2830},
  year={2011}
}

