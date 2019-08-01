from functools import wraps

from app import ENVIRONMENT



def verify_mode_variable(function):
    """
    Decorator that verifies MODE variable
    Returns:
        error due to invalid or missing MODE variable
    """
    @wraps(function)
    def decorated():
        error = None
        if not ENVIRONMENT:
            error = "You need to provide MODE variable"

        if ENVIRONMENT not in ['files', 'files_and_folders']:
            error = "MODE variable must be set to files or files_and_folders"

        return function(error)
    return decorated

def recursive_query_maker(function):
    """
    Decorator that cretes query based on MODE variable
    for recursive function
    Args:
        tree: tree class instance passed to get tree.root value
    Returns:
        query for retrieving new node data
    """
    @wraps(function)
    def decorated(tree):
        tree_root = tree.root
        if ENVIRONMENT == 'files':
            query = {
                "query" : {
                    "match" : {
                        "_id" : tree_root
                    }
                }
            }
        else:
            query = {
                "query": {
                    "multi_match" : {
                        "query" : tree_root,
                        "fields" : ["_id", "DS_Parent"]
                    }
                }
            }
        return function(tree, query)
    return decorated
