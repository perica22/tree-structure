from flask import request, jsonify

from app import APP
from app import ES

from app.tree_service import Tree
from app.auth import recursive_query_maker, verify_mode_variable, merge_sort



@APP.route("/search", methods=["POST"])
@verify_mode_variable
def search_api(error):
    """
    search API route returning tree structure of files and folders
    """
    if error:
        return jsonify({"error": error})

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

    # instance of tree class
    tree = Tree(leafs=search)

    for file in tree.leafs:
        nodes = [tree.create_node(file)]

        # calling this function recursivly to create tree
        create_tree(tree)
        tree.add_node(nodes)

        # resetting tree settings
        tree.reset_values()

    return jsonify(tree.structure), 200


@recursive_query_maker
def create_tree(tree, query=None):
    """
    Called recursivly to create tree structure
    """
    nodes = []

    search = ES.search(index="documents", body=query)["hits"]["hits"]
    search = merge_sort(search)
    for file in search:
        if file['_source']['DS_Type'] != 'file':
            node = tree.create_node(file)
            nodes.append(node)

    # base case for recursion
    if tree.root == 'null':
        return tree.add_node(nodes)

    structure = create_tree(tree)
    tree.add_node(nodes)

    return structure



if __name__ == "__main__":
    APP.run(host="0.0.0.0", debug=True)
