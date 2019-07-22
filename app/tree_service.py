import ipdb


# global list of id’s to keep track of already added files to tree,
# so we could skip searching for those which are not added
#TREE_FILES = ["null"] # TO-DO: make this redis list at some point


class Tree:
    def __init__(self, root, leafs):
        self.root = root
        self.master = None # maybe when i am doing this init i could do init of Node and add it to branch 
        self.branch = None
        self.node = None
        self.leafs = leafs

    def create_node(self, data):
        self.node = data["_source"]
        self.node["_id"] = data["_id"]
        if self.node["DS_Type"] == "dir":
            self.node["children"] = []

    def add_node(self, obj, mode=None):
        if not self.branch:
            self.branch = obj
        elif mode:
            [self.branch].append(obj)
        elif "children" in obj:
            obj["children"].append(self.branch)
            self.branch = obj
        
        self.root = self.branch["DS_Parent"]

    def _find_node(self, _id):
        item = self.master
        while item["_id"] != self.branch["DS_Parent"]:
            item = item["children"][0]

        return item

    def merge(self): # here you should accept master and branch value 
        if not self.master:
            self.master = self.branch
            self.branch=None
        else:
            master_item = self.master['children']
            branch_item = self.branch['children']
            files_to_add = []
            
            while branch_item != []:
                stop = False
                for master_file in master_item:
                    for branch_file in branch_item:
                        if master_file['_id'] in branch_file['_id']:
                            master_item = master_file['children']
                            stop = True
                            break
                        else:
                            files_to_add.append(branch_file)
                    if stop:
                        break
                for file in files_to_add:
                    master_item.append(file)
                    if 'children' in file:
                        self.branch = None
                        return    
                files_to_add = []
                try: 
                    branch_item = branch_file['children']
                except KeyError:
                    self.branch = None
                    return
