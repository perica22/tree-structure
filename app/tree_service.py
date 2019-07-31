
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

        self._determine_root(node)

        return node

    def _determine_pointer(self, node):
        """
        Changing tree pointer based on new node values
        """
        for file in self.pointer:
            if file['_id'] == node['DS_Parent']:
                self.previous_pointer = self.pointer
                self.pointer = file['children']

    def reset_values(self):
        """
        Resetting tree values
        """
        self.pointer = self.structure
        self.root = None

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
                    self._determine_pointer(node)

                file_already_in_tree = False
                for file in self.pointer:
                    if file['_id'] == node['_id']:
                        file_already_in_tree = True
                        break
                if not file_already_in_tree:
                    self.pointer.append(node)

    def _determine_root(self, node):
        """
        Setting tree root after each new node created
        """
        if not self.root:
            self.root = int(node['DS_Parent'])
        elif node["DS_Parent"] != 'null' and self.root != 'null':
            self.root = int(node["DS_Parent"]) if self.root > int(node["DS_Parent"]) else self.root
        else:
            self.root = 'null'
