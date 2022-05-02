from pickletools import string1
import pandas as pd
from ete3 import NCBITaxa
from pyparsing import string_start
ncbi = NCBITaxa()



class TreeClass:

    #LOOK AT DATA BEFOREHAND TO SEE WHAT THE HEADERS OF ROWS ARE
    '''
    @param: taxid- head of ncbi_tree, df- made from file, tax_col- name of taxid col in file
    sets variables then calls function to build the tree of samples 
    '''
    def __init__(self, taxid, df, tax_col):
        self.ncbi_tree = ncbi.get_descendant_taxa(taxid, return_tree=True)
        self.df = df;
        #self.meta_dict = self.df[tax_col].value_counts()
        self.meta_dict = self.df[tax_col]
        self.build_sample_tree()
        #print(self.ncbi_tree)
        # make better tree
    
    #private? 
    '''
    using postorder to traversal to build tree of taxid nodes, s.t. self_samples is
    number of samples of that taxid and total_samples is number of sampels of that taxid +
    its children's total_samples
    '''
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
    '''
    prints number of samples every taxid has in the tree
    '''
    def print_samples(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            print(curr_node.self_samples)
    '''
    prints the accumulative number of samples every taxid has in the tree
    using total_samples
    '''
    def print_total_samples(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            print(curr_node.total_samples)

    '''
    prints "taxid: [number of respective accumulated samples]" for all non-zero
    total_samples in tree
    '''
    def print_taxids_per_sample(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            if curr_node.total_samples != 0:
                #print(curr_node.taxid)
                print(curr_node.taxid + ": " + curr_node.total_samples)

    '''
    @param: taxid we want to see its total_samples, return_samples bool
    @return: when return_samples=True, return int taxid.total_samples,
            when False, return PhyloNode,
            return False if taxid is not in tree
    ''' 
    def look_up_taxid(self, taxid, return_samples=True):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            if taxid == curr_node.taxid: 
                #print(f"taxon id: {taxid}, number of self-samples: {curr_node.self_samples}, sum of self and child samples: {curr_node.total_samples}")
                if return_samples: 
                    return curr_node.total_samples
                else: 
                    return curr_node
        return False #null? 

    '''
    @param: taxid we want to look up
    @return: True if samples>20 s.t. taxid should be considered
    '''
    def decision(self, taxid):
        samples = self.look_up_taxid(taxid)
        if samples > 20:
            return True
        else:
            return False

        

    '''
    HELPER FUNCTION (kinda):
    @param: node which we want all it's children and grandchildren
    @return: set of that subtree
    '''
    def make_clade_set(self, node):
        clade = set()
        return_bool = False 
        root_type = self.look_up_taxid(node, return_samples=False)
        #for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
        #    if taxid == curr_node.taxid: 
        if root_type == False:
            print("This taxid node is not in tree")
            return return_bool
        for curr_node in root_type.traverse(strategy="preorder"):
            clade.add(curr_node.taxid) 
        return clade
    
    '''
    same as make_clade() without checks if we have that taxid in tree
    '''
    def faster_make_clade(self, node):
        clade = set()
        for curr_node in node.traverse(strategy="preorder"):
            clade.add(curr_node.taxid) 
        return clade
    '''
    make_clade without error checks but only has nodes which we have enough data on
    '''
    def fast_filtered_clade(self, node):
        clade = set()
        for curr_node in node.traverse(strategy="preorder"):
            if self.decision(curr_node):
                clade.add(curr_node.taxid) 
        return clade

    #pandas series to describe class labels - two: is/isnt in clade
    # up tree aggregation using sets and the stuff daniel put in terminal 

    #clade = current -> leafs 
    #clade = current -> leafs 
    '''
    @param: taxid is species we want to see is in clade in which node 
    is a root
    @return: true if taxid is in node's tree

    '''
    def in_clade(self, taxid, node):
        clade = self.make_clade(node)
        for node in clade:
            if node == taxid:
                return True
        return False 

    '''
    @param: node is root of subtree set, id_col is string of tsv's id column's name
    @return: list of indentifiers from tsv in node's subtree
    # "sample_id" in this instance
    '''
    def get_identifiers(self, node, id_col):
        clade_set = self.make_clade_set(node)
        rows = self.df[self.meta_dict.isin(clade_set)]
        
        identifiers = rows[id_col]
        return identifiers
        #returns the subset of rows that correspond to set of given taxids
         
    '''
    return boolean list corresponding to rows
    '''
    def get_bool(self, node):
        clade_set = self.make_clade_set(node)
        return self.meta_dict.isin(clade_set).astype(str)
        
    '''
    return boolean list not corresponding to rows
    '''
    def get_not_bool(self, node):
        clade_set = self.make_clade_set(node)
        return ~self.meta_dict.isin(clade_set).astype(int)
        rows = self.df[~self.meta_dict.isin(clade_set)]
        return rows

    '''
    @param: node is root of subtree set, id_col is string of tsv's id column's name
    @return: list of indentifiers NOT in tsv from node's subtree 
    '''
    def get_not_identifiers(self, node, id_col): 
        clade_set = self.make_clade_set(node)
        rows = self.df[~self.meta_dict.isin(clade_set)]
        non_identifiers = rows[id_col]
        return non_identifiers
        
    def get_tree(self):
        return self.ncbi_tree

'''
df = pd.read_csv('metadata.tsv', sep='\t') 
#print(len(df.index))
real_tree = 7742 #where should we start? vertebrae = 7742 
ncbi_tree = TreeClass(real_tree, df, 'ncbi_taxon_id')
print(ncbi_tree.get_bool(7742))



#homo_dict = {9605: 2, 9606: 3, 2665953:10}
#homo_tree = "homo"
#ncbi_tree = TreeClass(homo_tree, homo_dict) 

ncbi_tree = TreeClass(real_tree, df, 'ncbi_taxon_id')
ncbi_tree.build_sample_tree()
print("ALL SAMPLES")
ncbi_tree.print_samples()
print("ALL SAMPLE SUMS")
ncbi_tree.print_total_samples()
print("NON-ZERO SAMPLE SUMS")
ncbi_tree.print_taxids_per_sample()

ncbi_tree.look_up_taxid(9606)
print(ncbi_tree.decision(9606))
print(ncbi_tree.in_clade(2665953, 9606))
print(ncbi_tree.get_identifiers(9606, 'sample_name'))
'''