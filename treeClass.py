
import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()



class TreeClass:

    def __init__(self, taxid, meta_data_dict):
        self.meta_dict = meta_data_dict
        self.ncbi_tree = ncbi.get_descendant_taxa(taxid, return_tree=True)
        self.build_sample_tree()
        print(self.ncbi_tree)
        # make better tree
    
    #private? 
    def build_sample_tree(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
        
            if curr_node.is_leaf(): 
                if curr_node.taxid in self.meta_dict: 
                    curr_node.self_samples = self.meta_dict[curr_node.taxid]
                    curr_node.total_samples = self.meta_dict[curr_node.taxid]
                else:
                    curr_node.self_samples = 0
                    curr_node.total_samples = 0
            else:
                if curr_node.taxid in self.meta_dict: 
                    curr_node.self_samples = self.meta_dict[curr_node.taxid]
                else:
                    curr_node.self_samples = 0
                
                sample_sum = curr_node.self_samples
                for children in curr_node.get_children():
                    sample_sum+= children.total_samples
                curr_node.total_samples = sample_sum
    #maybe do for small ones only 
    def print_samples(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            print(curr_node.self_samples)

    def print_total_samples(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            print(curr_node.total_samples)

    def print_taxids_per_sample(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            if curr_node.total_samples != 0:
                #print(curr_node.taxid)
                print(curr_node.taxid)
                print(curr_node.total_samples)
    
    #lookup function
        #parameter: taxid 
        #return samples 
    #when return_samples is True, return int total_samples,
    #when False, return PhyloNode 
    def look_up_taxid(self, taxid, return_samples=True):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            if taxid == curr_node.taxid: 
                print(f"taxon id: {taxid}, number of self-samples: {curr_node.self_samples}, sum of self and child samples: {curr_node.total_samples}")
                
                if return_samples: 
                    return curr_node.total_samples
                else: 
                    return curr_node
        return False #null? 

    #decision function
        #if bool node.construct_model (total_samples > 50??? keep it fixed)
    #self_samples is a boolean, true when self, false when total
    def decision(self, taxid):
        
        samples = self.look_up_taxid(taxid)
        if samples > 20:
            return True
        else:
            return False

        
    #pandas series to describe class labels - two: is/isnt in clade
    # up tree aggregation using sets and the stuff daniel put in terminal 

    #clade = current -> leafs 
    #clade = current -> leafs 
    def in_clade(self, taxid, node):
        clade = self.make_clade(node)
        for node in clade:
            if node == taxid:
                return True
        return False 


    #return clade as set 
    def make_clade_set(self, node):
        clade = set()
        return_bool = False 
        root_type = self.look_up_taxid(node, return_samples=False)
        if root_type == False:
            print("This taxid node is not in tree")
            return return_bool
        for curr_node in root_type.traverse(strategy="preorder"):
            clade.add(curr_node.taxid) 
        return clade

    

df = pd.read_csv('metadata.tsv', sep='\t') 
meta_dict = df['ncbi_taxon_id'].value_counts()
homo_dict = {9605: 2, 9606: 3, 2665953:10}
homo_tree = "homo"
real_tree = 7742 #where should we start? vertebrae = 7742 

ncbi_tree = TreeClass(homo_tree, homo_dict)
#ncbi_tree = TreeClass(real_tree, meta_dict)
#ncbi_tree.build_sample_tree()
print("ALL SAMPLES")
#ncbi_tree.print_samples()
print("ALL SAMPLE SUMS")
#ncbi_tree.print_total_samples()
print("NON-ZERO SAMPLE SUMS")
ncbi_tree.print_taxids_per_sample()

ncbi_tree.look_up_taxid(9606)
print(ncbi_tree.decision(9606))
print(ncbi_tree.in_clade(2665953, 9606))