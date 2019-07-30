
class Tree:
    def __init__(self, leafs):
        self.root = None
        self.structure = []
        self.leafs = leafs
        self.pointer = None

    def create_node(self, data):
        """
        Creating node for tree
        """
        node = data["_source"]
        node["_id"] = data["_id"]
        if node["DS_Type"] == "dir":
            node["children"] = []
        if not self.root:
            self.root = node['DS_Parent']
        elif node["DS_Parent"] != 'null' and self.root != 'null':
            try:
                self.root = int(node["DS_Parent"]) if int(self.root) > int(node["DS_Parent"]) else int(self.root)
            except TypeError:
                self.root = node['DS_Parent']
        else:
            self.root = 'null'
        return node

    def add_node(self, nodes):
        """
        Adding note to tree structure
        """
        for node in nodes:
            if not self.structure:
                self.structure.append(node)
                self.pointer = self.structure
            else:
                if node['DS_Parent'] != self.pointer[0]['DS_Parent']:
                    for file in self.pointer:
                        if file['_id'] == node['DS_Parent']:
                            self.pointer = file['children'] # here we add it to same list as previous one
                # TODO this could be separate method
                file_already_in_tree = False # TODO can this be better ???
                for file in self.pointer:
                    if file['_id'] == node['_id']:
                        file_already_in_tree = True
                        #break
                if not file_already_in_tree:
                    self.pointer.append(node)
