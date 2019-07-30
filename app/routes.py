from app import APP
from app import ES
from app import ENVIRONMENT

from flask import request, jsonify

from app.tree_service import Tree
import ipdb


@APP.route("/search", methods=["POST"])
def search():
    if not ENVIRONMENT: # TODO make this to be decorator
        return jsonify({"error": "Please provide MODE variable"})
    # TODO make this decorator also
    query = {
            "query" : {
                "wildcard" : {
                   "DS_Name" : "{}".format(request.json)
            }}}
    search = ES.search(index="documents", body=query)["hits"]["hits"]
    if not search:
        return jsonify([]), 200

    # instance of tree class

    tree = Tree(leafs=search)
    for file in tree.leafs:
        tree.root = None
        node = tree.create_node(file)
        nodes = []
        nodes.append(node)
        # calling this function recursivly to create tree
        structure = create_tree(tree, node)
        tree.add_node(nodes)
        # resetting tree pointer to top of tree
        tree.pointer = tree.structure

    return jsonify(tree.structure), 200


def create_tree(tree, node=None):
    nodes = []
    query = {"query": {"match": {"_id": tree.root}}}# can be function decorator whihc would pass query here
    search = ES.search(index="documents", body=query)["hits"]["hits"]
    if ENVIRONMENT == 'files':
        query = {
                  "query" : {
                    "bool" : {
                      "must" : {
                        "term" : { "DS_Parent" : tree.root }
                      },
                      "must_not" : {
                        "term" : { "DS_Type": "file"}
                }}}}
        search_folders = ES.search(index="documents", body=query)["hits"]["hits"]
        for folder in search_folders:
            search.append(folder)

    for file in search:
        node = tree.create_node(file)
        nodes.append(node)

    # base case for recursion
    if tree.root == 'null':
        return tree.add_node(nodes)
    print(tree.structure)
    structure = create_tree(tree)
    tree.add_node(nodes)
    return structure


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
