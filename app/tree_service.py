
class Tree:
    """
    Class handling tree structure creation
    Args:
        root: current root folder of tree
        structure: represents final tree structure
        leafs: files from inital query(bottom of tree paths)
        pointer: place for adding new tree node
    """
    def __init__(self, leafs):
        self.root = None
        self.structure = []
        self.leafs = leafs
        self.pointer = self.structure

    def create_node(self, data):
        """
        Creates tree node
        Args:
            data: query result used to create node
        Returns:
            new tree node
        """
        node = data["_source"]
        node["_id"] = data["_id"]
        if node["DS_Type"] == "dir":
            node["children"] = []

        self._determine_root(node['DS_Parent'])

        return node

    def _determine_pointer(self, node):
        """
        Changes tree pointer based on new node values
        Args:
            node: tree node that needs to be added to structure
        """
        for file in self.pointer:
            if file['_id'] == node['DS_Parent']:
                self.pointer = file['children']

    def reset_values(self):
        """
        Resetting tree root and pointer values
        """
        self.pointer = self.structure
        self.root = None

    def add_node(self, nodes):
        """
        Addes node to tree structure
        Args:
            nodes: list of tree nodes that needs to be added to structure
        """
        for node in nodes:
            if not self.structure:
                self.structure.append(node)
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

    def _determine_root(self, new_parent):
        """
        Setting tree root after each new node created
        Args:
            new_parent: value of new tree root
        """
        if not self.root:
            self.root = int(new_parent)
        elif new_parent != 'null' and self.root != 'null':
            if self.root > int(new_parent):
                self.root = int(new_parent)
        else:
            self.root = 'null'
