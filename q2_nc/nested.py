from inspect import Arguments
from importlib_metadata import metadata
import pandas as pd
from ete3 import NCBITaxa
from unifrac import meta
ncbi = NCBITaxa()

from thefinalbattle import Finale
import theendgame import Training
import qiime_code
import biom
import qiime2 

import sys, getopt

#h = help
#t = train
#c = classify 
def main(argv):
   train = False
   classify = True

   metadata = ''
   metadata_c = ''
   metadata_t = ''

   feature_table = ''

   folder = ''
   folder_c = ''
   folder_t = ''

   human_table = ''
   try:
      opts, args = getopt.getopt(argv,"ht:c:",["train=","classify="])
   except getopt.GetoptError:
      #print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   j = 0
   for i in range(opts):
      if opts[i] == '-h':
         print('nested.py -t/--train <metadata.tsv> <feature_table.qza> <folder> -c/--classify <metadata.tsv> <human_feature_table.qza> <folder>')
         sys.exit()
      elif opts[i] in ("-t", "--train"):
         #meta
         #ft
         #folder
         metadata_c = args[j]
         j+=1 
         feature_table = args[j]
         j+=1 
         folder_c = args[j]
         j+=1
         train = True

      elif opts[i] in ("-c", "--classify"):
         #meta
         #human ft
         #folder

         metadata_t = args[j]
         j+=1 
         human_table = args[j]
         j+=1 
         folder_t = args[j]
         j+=1 
         classify = True
   
   if train and classify: 
      if metadata_c == metadata_t: 
         metadata = metadata_t
      else: 
         print("complain error show metadatas bad")
         sys.exit(2)
      if folder_c == folder_t: 
         folder = folder_t
      else: 
         print("error error show folders bad")
         sys.exit(2)
   if train:
      #make sure folder and files exists 
      folder = folder_t
      metadata = metadata_t

      train = Training(metadata, feature_table, folder)
      train.train()
      #call rest of the file?? 

   if classify: 
      folder = folder_c
      metadata = metadata_c

      finishing_up = Finale(feature_table, metadata, folder)
      taxid = finishing_up.recursive(finishing_up.root()) 
      print(taxid)
      #call the next file ?? 
      

   else:
      print("how did we get here")
      #make sure folder and files exists 


   #print 'Input file is "', inputfile
   #print 'Output file is "', outputfile

if __name__ == "__main__":
   main(sys.argv[1:])

