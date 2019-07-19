import ipdb


# global list of id’s to keep track of already added files to tree,
# so we could skip searching for those which are not added
TREE_FILES = ["null"] # TO-DO: make this redis list at some point


class Tree:
    def __init__(self, root, leafs):
        self.root = root
        self.master = None # maybe when i am doing this init i could do init of Node and add it to branch 
        self.branch = None
        self.node = None
        self.leafs = leafs
        #self.mode = mode

    def create_node(self, data):
        self.node = data["_source"]
        self.node["_id"] = data["_id"]
        if self.node["DS_Type"] == "dir":
            self.node["children"] = []

    def add_node(self, obj, mode=None):
        if not self.branch:
            self.branch = obj
        elif mode:
            self.branch['children'].append(obj)
        elif "children" in obj:
            obj["children"].append(self.branch)
            self.branch = obj
        
        self.root = self.branch["DS_Parent"]
        TREE_FILES.append(obj["_id"])

    def _find_node(self, _id):
        item = self.master
        while item["_id"] != self.branch["DS_Parent"]:
            item = item["children"][0]

        return item

    def merge(self, _id):
        if not self.master:
            self.master = self.branch
            self.branch=None
        else:
            place_to_merge = self._find_node(_id)
            place_to_merge["children"].append(self.branch)
            self.branch=None