
tree_structure = {
        "DS_Name": "folder1",
        "DS_Parent": "null",
        "DS_Type": "dir",
        "_id": "1",
        "children": [
            {
                "DS_Name": "folder2",
                "DS_Parent": "1",
                "DS_Type": "dir",
                "_id": "2",
                "children": [
                    {
                        "DS_Name": "folder4",
                        "DS_Parent": "2",
                        "DS_Type": "dir",
                        "_id": "4",
                        "children": [
                            {
                                "DS_Name": "a.txt",
                                "DS_Parent": "4",
                                "DS_Type": "file",
                                "_id": "6"
                            }
                        ]
                    }
                ]
            }
        ]
    }


place_to_merge = {
        "DS_Name": "folder1",
        "DS_Parent": "null",
        "DS_Type": "dir",
        "_id": "1",
        "children": [
            {
                "DS_Name": "folder2",
                "DS_Parent": "1",
                "DS_Type": "dir",
                "_id": "2",
                "children": [
                    {
                        "DS_Name": "folder4",
                        "DS_Parent": "2",
                        "DS_Type": "dir",
                        "_id": "4",
                        "children": []}]}]}

branch = {"DS_Name": "sdfas.txt",
        "DS_Parent": "2",
        "DS_Type": "file",
        "_id": "8"}

new_tree = tree_structure[place_to_merge].append(branch)

print(json.dumps(new_tree, indent=4))
'''
item = tree_structure
while item['_id'] != branch['DS_Parent']:
	item = item['children'][0]


item['children'].append(branch)
import json

print(json.dumps(tree_structure, indent=4))
'''