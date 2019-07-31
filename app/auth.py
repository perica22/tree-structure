from app import ENVIRONMENT

from functools import wraps



def verify_mode_variable(function):
    """
    Decorator verifying MODE variable
    """
    @wraps(function)
    def decorated():
        if not ENVIRONMENT:
            return jsonify({"error": "You need to provide MODE variable"})

        if ENVIRONMENT not in ['files', 'files_and_folders']:
            return jsonify({"error": "MODE variable must be set to files or files_and_folders"})

        return function()
    return decorated

def recursive_query_maker(function):
    """
    Decorator creting query based on MODE variable
    for recursive function
    """
    @wraps(function)
    def decorated(tree):
        if ENVIRONMENT == 'files':
            query = {"query": {"match": {"_id": tree.root}}}
        else:
            query =  {
                      "query": {
                        "multi_match" : {
                          "query": tree.root, 
                          "fields": [ "_id", "DS_Parent" ] 
                        }
                      }
                    }
        return function(tree, query)
    return decorated

def merge_sort(collection):
    """
    Merge sort function for sorting values that we get
    after querying DB in recursion part
    """
    length = len(collection)
    if length > 1:
        midpoint = length // 2
        left_half = merge_sort(collection[:midpoint])
        right_half = merge_sort(collection[midpoint:])
        i = 0
        j = 0
        k = 0
        left_length = len(left_half)
        right_length = len(right_half)
        while i < left_length and j < right_length:
            if int(left_half[i]['_id']) < int(right_half[j]['_id']):
                collection[k] = left_half[i]
                i += 1
            else:
                collection[k] = right_half[j]
                j += 1
            k += 1

        while i < left_length:
            collection[k] = left_half[i]
            i += 1
            k += 1

        while j < right_length:
            collection[k] = right_half[j]
            j += 1
            k += 1

    return collection
