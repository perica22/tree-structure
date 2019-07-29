from app import APP
from app import ES
from app import ENVIRONMENT

from flask import request, jsonify

from app.tree_service import Tree, TREE_FILES
import ipdb
        

@APP.route("/search", methods=["POST"])
def search():
    if not ENVIRONMENT:
        return jsonify({"error": "Please provide MODE variable"})

    query = {
            "query" : {
                "wildcard" : {
                   "DS_Name" : "*{}*".format(request.json)
            }}}
    search = ES.search(index="documents", body=query)["hits"]["hits"]
    if not search:
        return jsonify([]), 200

    # instance of tree class
    tree = Tree(root=search[0]["_source"]["DS_Parent"], leafs=search)

    for file in tree.leafs:
        node = make_branch(file, tree)
        #print(tree.branch)

    return jsonify([tree.branch]), 200


def make_branch(file, tree):
    query = {"query": {"match": {"_id": tree.root}}}
    search = ES.search(index="documents", body=query)

    node = tree.create_node(search["hits"]["hits"][0])
    if tree.root == 'null':
        print("Returning to previous frame...!")
        return tree.add_node(node)

    result = make_branch(file, tree)
    tree.add_node(node)
    return result
     



























def search_folders(tree):
    """
    Searching for additonal folders in case of
    filse_and_folders MODE
    """
    query = {
              "query": {
                "bool" : {
                  "must" : {
                    "term" : { "DS_Parent" : tree.node['_id'] }
                  },
                  "must_not" : {
                    "term": { "DS_Type": "file"}
            }}}}
    search = ES.search(index="documents", body=query)

    for file in search['hits']['hits']:
        if file['_id'] not in TREE_FILES:
            tree.create_node(file)
            tree.folders_list.append(tree.node)



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
