import ipdb

class Node:
    def __init__(self, data):
        self.data = data
        if self.data['DS_Type'] == 'dir':
            data['children'] = []

class Tree:
    def __init__(self):
        self.root = None
        self.structure = None

    def add_child(self, obj):
        self.structure['children'].append(obj)
# TODO:
# 1. sort list by their id
# 2. add root folder firstly
# 3. take next one and check its parent id
# 4. search folder with that id
# 5. add file to his children

data = [{
            "_id": "1",
            "DS_Name": "folder1",
            "DS_Type": "dir",
            "DS_Parent": "null",
        },
        {
            "_id": "2",
            "DS_Name": "folder2",
            "DS_Type": "dir",
            "DS_Parent": "1",
        },
        {
            "_id": "3",
            "DS_Name": "a.txt",
            "DS_Type": "file",
            "DS_Parent": "1",
        }]

tree = Tree()
ipdb.set_trace()
for doc in data:

    node = Node(doc)

    if not tree.root:
        tree.root = node.data['_id']
        tree.structure = node.data
    else:
        tree.add_child(node.data)
        if node.data['DS_Type'] == 'dir':
            tree.root = node.data['_id']


print(tree.__dict__['structure'])
