
class Node:
    def __init__(self, data):
        self.data = data['_source']
        self.data['_id'] = data['_id']
        if self.data['DS_Type'] == 'dir':
            self.data['children'] = []

class Tree:
    def __init__(self):
        self.root = None
        self.structure = None

    def add_child(self, obj):
        if not self.structure:
            self.structure = obj
            self.root = self.structure['DS_Parent']
        else:
            obj['children'].append(self.structure)
            self.structure = obj
            self.root = self.structure['DS_Parent']
