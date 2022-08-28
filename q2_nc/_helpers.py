import pandas as pd
from ete3 import NCBITaxa
ncbi = NCBITaxa()


class TreeClass:

    '''
    @param: taxid- head of ncbi_tree, df- made from file, tax_col- name of taxid col in file
    sets variables then calls function to build the tree of samples 
    '''
    def __init__(self, taxid, df, tax_col):
        self.ncbi_tree = ncbi.get_descendant_taxa(taxid, return_tree=True)
        self.df = df;
        #self.meta_dict = self.df[tax_col].value_counts()
        self.meta_dict = self.df[tax_col]
        self.count_dict = self.meta_dict.value_counts()
        
        self.build_sample_tree()
    

    '''
    using postorder to traversal to build tree of taxid nodes, s.t. self_samples is
    number of samples of that taxid and total_samples is number of sampels of that taxid +
    its children's total_samples
    '''
    def build_sample_tree(self):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
        
            if curr_node.is_leaf(): 
    
                if curr_node.taxid in self.count_dict: 
                    curr_node.self_samples = self.count_dict[curr_node.taxid]
                    curr_node.total_samples = self.count_dict[curr_node.taxid]
                else:
                    curr_node.self_samples = 0
                    curr_node.total_samples = 0
            else:
                if curr_node.taxid in self.count_dict:
                    curr_node.self_samples = self.count_dict[curr_node.taxid]
                else:
                    curr_node.self_samples = 0
                
                sample_sum = curr_node.self_samples
                for children in curr_node.get_children():
                    sample_sum+= children.total_samples
                curr_node.total_samples = sample_sum
  

    '''
    @param: taxid 
    @return: return PhyloNode of taxid,
            return False if taxid is not in tree
    ''' 
    def get_node(self, taxid):
        for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
            if taxid == curr_node.taxid: 
                #print(f"taxon id: {taxid}, number of self-samples: {curr_node.self_samples}, sum of self and child samples: {curr_node.total_samples}")
                return curr_node
        return False #null? 

    '''
    @param: taxid we want to look up
    @return: True if samples>20 s.t. taxid should be considered
    '''
    def decision(self, taxid):
        samples = self.get_samples(taxid)
        if samples > 20:
            return True
        else:
            return False

    '''
    @param: node we want samples of
    @return: # total sampes or -1 if doesn't exist
    '''
    def get_samples(self, node):
        try:
            val = node.total_samples
        except: 
            val = -1
        return val     

    '''
    @param: taxid as parent and taxid_column
    @return: 
    '''
    def get_taxids(self, taxid, tax_col):
        node = self.get_node(taxid)
        clade_set = self.make_clade_set(node)
        rows = self.df[self.meta_dict.isin(clade_set)]
        taxids = rows[tax_col]
        tax_set = (set(taxids))
        taxids = (pd.DataFrame(tax_set))
        return taxids


    '''
    HELPER FUNCTION (kinda):
    @param: node which we want all it's children and grandchildren
    @return: set of that subtree
    '''
    def make_clade_set(self, node):
        clade = set()
        check = self.get_samples(node)
        #for curr_node in self.ncbi_tree.traverse(strategy="postorder"):
        #    if taxid == curr_node.taxid: 
        if check == -1:
            raise ValueError('This taxid node does not exist in the tree')
        for curr_node in node.traverse(strategy="preorder"):
            clade.add(curr_node.taxid) 
        return clade
    

    '''
    @param: query is the node of a species we want to see is in clade in which node 
    is a root
    @return: true if taxid is in node's tree

    '''
    def in_clade(self, query, node):
        clade = self.make_clade(node)
        for node in clade:
            if node == query:
                return True
        return False 

    '''
    @param: node is root of subtree set, id_col is string of tsv's id column's name
    @return: list of indentifiers from tsv in node's subtree
    # "sample_id" in this instance
    '''
    def get_identifiers(self, taxid, id_col):
        node = self.get_node(taxid, return_samples=False)
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
        return ~self.meta_dict.isin(clade_set).astype(str)

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
    
    def get_root(self):
        return self.ncbi_tree.get_tree_root()
    
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



