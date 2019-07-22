master = {
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
                           }]}]}]}
branch = {
       "DS_Name": "folder1",
       "DS_Parent": "null",
       "DS_Type": "dir",
       "_id": "1",
       "children": [
           {
               "DS_Name": "folder10",
               "DS_Parent": "1",
               "DS_Type": "dir",
               "_id": "10",
               "children": []
           },
           {
               "DS_Name": "abcd.txt",
               "DS_Parent": "1",
               "DS_Type": "file",
               "_id": "15"
            },
           {
               "DS_Name": "folder2",
               "DS_Parent": "1",
               "DS_Type": "dir",
               "_id": "2",
               "children": [
                   {
                       "DS_Name": "sdfas.txt",
                       "DS_Parent": "2",
                       "DS_Type": "file",
                       "_id": "8"
                   },
                   {
                       "DS_Name": "folder4",
                       "DS_Parent": "2",
                       "DS_Type": "dir",
                       "_id": "4",
                       "children": []}]}]}
import json
import ipdb
master_item = master['children']
branch_item = branch['children']
files_to_add = []
while branch_item != []:
   for master_file in master_item:
       for branch_file in branch_item:
           if master_file['_id'] in branch_file['_id']:
               continue
           else:
               files_to_add.append(branch_file)
   for file in files_to_add:
       master_item.append(file)    
   files_to_add = []
   master_item = master_file['children']
   branch_item = branch_file['children']
print(json.dumps(master, indent=4))