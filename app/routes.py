from app import APP
from app import ES
from app import ENVIRONMENT

from flask import request, jsonify

from app.tree_service import    Tree, TREE_FILES

import ipdb



@APP.route("/search", methods = ["POST"])
def search():
    if not ENVIRONMENT: # could be a decoretor
        return jsonify({"error": "Please provide MODE variable"})

    query = {
                "query" : {
                    "wildcard" : {
                       "DS_Name" : "*{}*".format(request.json)
                    }
                }
            }
    search = ES.search(index="documents", body=query)["hits"]["hits"]

    if not search:
        return jsonify([]), 200

    tree = Tree(root=search[0]["_source"]["DS_Parent"], leafs=search) #mode=ENVIRONMENT)

    for file in tree.leafs:
        node = tree.create_node(file)
        tree.add_node(tree.node)

        while tree.node["DS_Parent"] not in TREE_FILES: # or node.data["DS_Parent"] != "null"
            # searching for next folder in branch
            query = {"query": {"match": {"_id": tree.root}}}
            # maybe i should query by must {_id: tree.root} and must {DS_Parent: tree.root} and must_not {DS_Type: file} which would return all folders from that file
            # add them all to branch and save to TREE_FILES only those which are part of tree structure / not those which are added as part of folders mode variable
            search = ES.search(index="documents", body=query)

            node = tree.create_node(search["hits"]["hits"][0])
            tree.add_node(tree.node)

        # merging branch to master
        tree.merge(tree.node["DS_Parent"])

    return jsonify([tree.master]), 200



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


'''
if ENVIRONMENT == 'files_and_folders':
                pass
                query = {
                          "query": {
                            "bool" : {
                              "must" : {
                                "term" : { "DS_Parent" : tree.node['DS_Parent'] }
                              },
                              "must_not" : {
                                "term": {"DS_Type": "file"}
                              }}}}
                search = ES.search(index="documents", body=query)
                
                for file in search['hits']['hits']:
                   # ipdb.set_trace()
                    tree.create_node(file)
                    if tree.node["_id"] not in TREE_FILES:
                        #tree.create_node(file)
                        tree.add_node(tree.node, mode=True)
'''