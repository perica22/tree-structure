# elasticsearch---flask
# Task Description

Tree structure created by retrieving data from ElasticSearch using Flask App
You need to create tree search API with Python (Flask) and Elasticsearch. Let’s assume that we have following tree stored in Elasticsearch:
```
● folder1
   ❍ folder2
    ■ folder3
      ● aBc.txt
      ● ABb.txt
      ● xyz.txt
    ■ folder4
      ● Folder10
        ❍ oaxbco.pdf
        ❍ ddAb.doc
        ❍ folder111
          ■ file.pdf
          ■ fileab.zip
          ■ somefile.doc
          ■ fo.txt
        ■ Kkk.zip
        ■ Folder19
          ● Dd.doc
          ● Oacb.pdf
          ● Folder32
            ❍ Kab.pdf
            ❍ ygabe.docx
    ❍ kabcd.xls
    ❍ folder5
      ■ folder6
        ●folder88
          ❍ test.doc
        ● fo.docs
        ● xaby.txt
        ● lkAB.docx
       ■ qqa.docx
```       
       
Now when we search for term "ab" API should return following tree:
```
●folder1
  ❍ folder2
    ■ folder3
      ● aBc.txt
      ● ABb.txt
    ■ folder4
      ● Folder10
        ❍ ddAb.doc
        ❍ folder111
    ■ Folder19
      ● Folder32
        ❍ Kab.pdf
        ❍ ygabe.docx
  ❍ kabcd.xls
  ❍ folder5
    ■ folder6
      ● xaby.txt
      ● lkAB.docx
```      

## Elasticsearch
This is an example of Elastic mapping you should use to store files and dirs:
```
PUT documents
{
   "mappings": {
       "document": {
       "properties": {
            "DS_Name": {
               "type": "text"
         },
         "DS_Type": {
              "type": "keyword",
              "index": "not_analyzed"
         },
         "DS_Parent": {
              "type": "keyword",
              "index": "not_analyzed"
            }
         }
      }
   }
}
```
Where DS_Name represent file/dir name, DS_Type represent a "file" or "dir" and DS_Parent is _id
of parent dir where this file/dir is located (if DS_Parent is equal to null then it is root of the tree).

But you are not limited to this structure only rule is that you have parent field which represent _id
of parent directory of current file/dir. If you want to put some analyzer, change structure, addadditional fields, ... you can do that.


## API
API should contain one POST route called /search which expect following parameters:
```
{
  "query": "ab"
}
```
There are two modes for the search: - One will only search for files (MODE=files) - Other will search
both for files and folders (MODE=files_and_folders)

Which mode is active should be specified by providing environment variable MODE with one of
following values:
```
   ● files
   ● files_and_folders
```

## Example
if you search for "fo" in the above tree and if the MODE is equal to files result should be:
```
● folder1
  ❍ folder2
    ■ folder4
      ● Folder10
        ❍ folder111
          ■ fo.txt
  ❍ folder5
    ■ folder6
      ● fo.docs
```      
on the other hand if the *MODE* is equal to files_and_folders result should be:
```
● folder1
  ❍ folder2
    ■ folder3
    ■ folder4
      ● Folder10
        ❍ folder111
          ■ fo.txt

    ■ Folder19
      ● Folder32
  ❍ folder5
    ■ folder6
      ● folder88
      ● fo.docs
 ```     
      
## Example of API output
If following tree is result of search:
```
● folder1
  ❍ folder2
    ■ folder4
      ● a.txt
      ● b.txt
    ■ Folder19
    ■ c.txt
  ❍ folder5
    ■ d.docs
```
then API should return following JSON:
```
[
     {
          "_id": "1"
          "DS_Name": "folder1",
          "DS_Type": "dir",
          "DS_Parent": "null",
          "children": [
               {
                    "_id": "2",
                    "DS_Name": "folder2",
                    "DS_Type": "dir",
                    "DS_Parent": "1",
                    "children": [
                           {
                             "_id": "4",
                             "DS_Name": "folder4",
                             "DS_Type": "dir",
                             "DS_Parent": "2",
                             "children": [
                                    {
                                      "_id": "6",
                                      "DS_Name": "a.txt",
                                      "DS_Type": "file",
                                      "DS_Parent": "4",
                                      "children": []
                                    },
                                    {
                                      "_id": "7",
                                      "DS_Name": "b.txt",
                                      "DS_Type": "file",
                                      "DS_Parent": "4",
                                      "children": []
                                    },
                                 ]
                             },
                             {
                               "_id": "5",
                               "DS_Name": "Folder19",
                               "DS_Type": "dir",
                               "DS_Parent": "2",
                               "children": []
                             },
                             {
                               "_id": "8",
                               "DS_Name": "c.txt",
                               "DS_Type": "file",
                               "DS_Parent": "2",
                               "children": []
                             }
                           ]
                      },
                      {
                        "_id": "3",
                        "DS_Name": "folder5",
                        "DS_Type": "dir",
                        "DS_Parent": "1",
                        "children": [
                             {
                               "_id": "9",
                               "DS_Name": "d.docs",
                               "DS_Type": "file",
                               "DS_Parent": "3",
                               "children": []
                             }
                       ]
                  }
            ]
       }
 ]
``` 
 
## Docker

You must provide docker-compose.yml file which will start two containers:
● One for Elasticsearch
● One for Flask API

so app will be tested by running:
```
  docker-compose -f docker-compose.yml up -d --build
 ```
and then hitting API endpoint from the Postman tool. Keep in mind that your app will be run under
some VM so you must expose proper ports (You can use docker-machine in order to test your app).
