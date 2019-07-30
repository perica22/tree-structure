# global list of id’s to keep track of already added files to tree,
# so we could skip searching for those which are not added
TREE_FILES = ["null"] # TO-DO: make this redis list at some point


class Tree:
    def __init__(self, root, leafs):
        self.root = root
        self.master = None
        self.branch = None
        self.node = None
        self.leafs = leafs
        self.folders_list = []

    def create_node(self, data):
        """
        Creating node for tree
        """
        self.node = data["_source"]
        self.node["_id"] = data["_id"]
        if self.node["DS_Type"] == "dir":
            self.node["children"] = []

    def add_node(self, obj):
        """
        Adding note to tree structure
        """
        if not self.branch:
            self.branch = obj
        else:
            obj["children"].append(self.branch)
            self.branch = obj

        TREE_FILES.append(obj['_id'])
        self.root = self.branch["DS_Parent"]

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
