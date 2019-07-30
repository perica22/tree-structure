# global list of id’s to keep track of already added files to tree,
# so we could skip searching for those which are not added
TREE_FILES = ["null"] # TO-DO: make this redis list at some point


class Tree:
    def __init__(self, leafs):
        self.root = None
        self.structure = []
        self.leafs = leafs
        #self.folders_list = []
        self.pointer = None

    def create_node(self, data):
        """
        Creating node for tree
        """
        node = data["_source"]
        node["_id"] = data["_id"]
        if node["DS_Type"] == "dir":
            node["children"] = []

        self.root = node["DS_Parent"]

        return node

    def add_node(self, obj):
        """
        Adding note to tree structure
        """
        if not self.structure:
            self.structure.append(obj)
            self.pointer = self.structure
        else:  
            if obj['DS_Parent'] != self.pointer[0]['DS_Parent']:
                for file in self.pointer:
                    if file['_id'] == obj['DS_Parent']:
                        self.pointer = file['children'] # here we add it to same list as previous one 
                
            # TODO this could be separate method
            file_already_in_tree = False # TODO can this be better ???
            for file in self.pointer:
                if file['_id'] == obj['_id']:
                    file_already_in_tree = True
            if not file_already_in_tree:
                self.pointer.append(obj) 





















    def merge(self, master_item, branch_item):
        """
        Merging new branch to master which contans all 
        previous branches
        """
        if not self.master:
            self.master = self.branch
        else:
            pointer = None
            while 'children' in branch_item:
                for branch_file in branch_item['children']:
                    for master_file in master_item['children']:
                        if branch_file['_id'] == master_file['_id']:
                            pointer = master_file
                if self.folders_list: # in case filse_and_folders MODE
                    self._add_folders(master_item)
                if pointer:
                    master_item = pointer
                    branch_item = branch_file
                    pointer = None
                else:
                    master_item['children'].append(branch_file)

        self.branch = None

    def _add_folders(self, path):
        for folder in self.folders_list:
            if folder['DS_Parent'] == path['_id'] and folder['_id'] not in TREE_FILES:
                path['children'].append(folder)
                TREE_FILES.append(folder['_id'])
