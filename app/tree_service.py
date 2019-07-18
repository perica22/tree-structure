
class Node:
    def __init__(self, data):
        self.data = data['_source']
        self.data['_id'] = data['_id']
        if self.data['DS_Type'] == 'dir':
            self.data['children'] = []


class Tree:
    def __init__(self, root, leafs):
        self.root = root
        self.structure = None
        self.branch = None
        self.leafs = leafs

    def add_node(self, obj):
        obj['children'].append(self.structure)
        self.structure = obj
        self.root = self.structure['DS_Parent']

    def find_node(self, _id):
        item = self.tree_structure
        while item['_id'] != self.branch['DS_Parent']:
            item = item['children'][0]
