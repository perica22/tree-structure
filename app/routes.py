from app import APP
from app import ES
from app import ENVIRONMENT

from flask import request, jsonify

from app.tree_service import Tree, TREE_FILES
import ipdb


@APP.route("/search", methods=["POST"])
def search():
    if not ENVIRONMENT: # TODO make this to be decorator 
        return jsonify({"error": "Please provide MODE variable"})

    # TODO make this decorator also
    query = {
            "query" : {
                "wildcard" : {
                   "DS_Name" : "*{}*".format(request.json)
            }}}
    search = ES.search(index="documents", body=query)["hits"]["hits"]
    if not search:
        return jsonify([]), 200

    # instance of tree class
    tree = Tree(leafs=search)

    for file in tree.leafs:
        node = tree.create_node(file)

        # calling this function recursivly to create tree
        structure = create_tree(tree)
        tree.add_node(node)

        # resetting tree pointer to top of tree
        tree.pointer = tree.structure

    return jsonify(tree.structure), 200


def create_tree(tree):
    query = {"query": {"match": {"_id": tree.root}}}# can be function decorator whihc would pass query here 
    #try:
    search = ES.search(index="documents", body=query)["hits"]["hits"][0]

    node = tree.create_node(search)

    # base case for recursion
    if tree.root == 'null':
        return tree.add_node(node)

    structure = create_tree(tree)
    tree.add_node(node) 
    return structure



























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
