from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import numpy as np
from os import environ


app = Flask(__name__)
es = Elasticsearch()
ENVIRONMENT = environ.get("MODE", default=False)


@app.route('/search', methods = ['POST'])
def getAll():

	query = {"query": {"match": {"DS_Name": request.json}}}
	search_result = es.search(index='documents', body=query)


	if not search_result:
		return 'No matches found!'

	if ENVIRONMENT  == 'files_and_folders':
		my_path, my_folders = path_folders(search_result)

		sub_folders, result = tree_folders(my_path, my_folders)

		final_tree = sub_tree(sub_folders, result)

		return jsonify(final_tree)

	elif ENVIRONMENT  == 'files':
		my_path = path_files(search_result)

		result = tree_files(my_path)

		return jsonify(result)


	else:
		return jsonify({'error': 'Provide MODE variable'})



#CREATING TREE PATH
def path_files(search):

	hits = search['hits']['hits']
	total = search['hits']['total']

	main_root = []

	for i in range(total):

		leaf_root = []

		file = hits[i]['_source']
		parent = file['DS_Parent']

		leaf_root.append(int(hits[i]['_id']))

		while (parent != 'null'):
			#searching for next file in main_path
			search = es.search(index='documents', body={'query': {'match': {'_id': parent}}})
			hits2 = search['hits']['hits']
			file = hits2[0]['_source']

			# extracting id and parent folder for last file in search result
			id = hits2[0]['_id']
			parent = file['DS_Parent']

			# adding id to the path
			leaf_root.append(int(id))

		#sorting and andding id's to main_path
		leaf_root = sorted(list(leaf_root), reverse=False)
		main_root.append(leaf_root)

	main_root = np.array(main_root)


	return (main_root)



#CREATING TREE PATH FOR files_and_folders MODE
def path_folders(search):

	hits = search['hits']['hits']
	total = search['hits']['total']

	main_root = []
	folders = []

	for i in range(total):

		leaf_root = []

		file = hits[i]['_source']
		parent = file['DS_Parent']

		leaf_root.append(int(hits[i]['_id']))

		while (parent != 'null'):
			#searching for next file in main_path
			search = es.search(index='documents', body={'query': {'match': {'_id': parent}}})
			hits2 = search['hits']['hits']
			file = hits2[0]['_source']

			#searching for folder for files_and_folders MODE
			search2 = es.search(index='documents', body={'query': {'bool': {'must': [{'match': {'DS_Parent': parent}},
																					 {'match': {'DS_Type': 'dir'}}]}}})
			hits3 = search2['hits']['hits']
			for n in range(len(hits3)):
				folders.append(int(hits3[n]['_id']))

			# extracting id and parent folder for last file in search result
			id = hits2[0]['_id']
			parent = file['DS_Parent']

			# adding id to the path
			leaf_root.append(int(id))

		#sorting and andding id's to main_path
		leaf_root = sorted(list(leaf_root), reverse=False)
		main_root.append(leaf_root)

	#sorting folders for files_and_folders MODE
	folders = sorted(list(folders), reverse=False)

	#getting unique values in folders for files_and_folders MODE
	output = []
	for x in folders:
		if x not in output:
			output.append(x)

	main_root = np.array(main_root)


	return (main_root, output)



#CREATING TREE
def tree_files(main_root):
	files = []
	appended = []

	for i in range(len(main_root)):
		for j in range(len(main_root[i])):

			exists = False
			# searching for last file in main_root
			search = es.search(index='documents', body={'query': {'match': {'_id': str(main_root[i][j])}}})
			hits = search['hits']['hits'][0]
			id = hits['_id']

			# cheking if document with this id is already in files
			if i != 0:
				for n in appended:
					if n == int(id):
						# creating new root
						if id == '1':
							children_root = files[0]['children']
							exists = True
							break
						else:
							for x in range(len(children_root)):
								if children_root[x]['_id'] == id:
									children_root = children_root[x]['children']
									break
							exists = True
							break

				if exists == True:
					continue
				else:
					pass

			# creating dictionary with values for every unique document in main_root
			document = {}
			# adding files id and other informations to document
			for key, value in hits.items():
				if key == '_id':
					document[key] = value
					break

			source = hits['_source']
			for key, value in source.items():
				document[key] = value

			document['children'] = []

			# appending document to files and creating next root
			if id == '1':
				files.append(document)
				appended.append(int(id))
				children_root = files[0]['children']
			else:
				children_root.append(document)
				appended.append(int(id))
				children_root = document['children']


	return (files)


#CREATING TREE FOR files_and_folders MODE
def tree_folders(main_root, sub_folders):

	files = []
	appended = []

	for i in range(len(main_root)):
		for j in range(len(main_root[i])):

			exists = False
			#searching for last file in main_root
			search = es.search(index = 'documents', body = {'query': {'match': {'_id': str(main_root[i][j])}}})
			hits = search['hits']['hits'][0]
			id = hits['_id']

			#cheking if document with this id is already in files
			if i != 0:
				for n in appended:
					if n == int(id):
						#creating new root
						if id == '1':
							children_root = files[0]['children']
							exists = True
							break
						else:
							for x in range(len(children_root)):
								if children_root[x]['_id'] == id:
									children_root = children_root[x]['children']
									break
							exists = True
							break

				if exists == True:
					continue
				else:
					pass

			#creating dictionary with values for every unique document in main_root
			document = {}
			#adding files id and other informations to document
			for key, value in hits.items():
				if key == '_id':
					document[key] = value
					break

			source = hits['_source']
			for key, value in source.items():
				document[key] = value

			document['children'] = []

			#appending document to files and creating next root
			if id == '1':
				files.append(document)
				appended.append(int(id))
				children_root = files[0]['children']
			else:
				children_root.append(document)
				appended.append(int(id))
				children_root = document['children']

	#removing files from folders for files_and_folders MODE, which already have been added
	for i in appended:
		for j in sub_folders:
			if i == j:
				sub_folders.remove(j)


	return(sub_folders, files)



#ADDING FOLDERS FOR files_and_folders MODE
def sub_tree(sub_folders, files):

	for x in range(len(sub_folders)):

		# searching for last file in sub_folders
		search = es.search(index='documents', body={'query': {'match': {'_id': str(sub_folders[x])}}})
		hits = search['hits']['hits']
		file = hits[0]['_source']
		parent = file['DS_Parent']
		hits = search['hits']['hits'][0]

		# creating dictionary with values for every folder in sub_folders
		document = {}
		# adding files id and other informations to document
		for key, value in hits.items():
			if key == '_id':
				document[key] = value
				break

		source = hits['_source']
		for key, value in source.items():
			document[key] = value

		document['children'] = []

		#determininig root for document
		root = files[0]
		exists = False
		for m in range(int(parent)):
			if exists == True:
				break
			for key, value in root.items():
				if key == '_id':
					if value == parent:
						print(value)
						root['children'].append(document)
						exists = True
						break
				elif key == 'children':
					root = value
					root = root[0]


	return files




if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)