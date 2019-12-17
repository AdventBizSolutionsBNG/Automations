from pymongo import MongoClient
from pprint import pprint
import json
import os, sys
import traceback



def openDBConnection(_METADATA_DB_SERVER,_METADATA_DB_PORT ,_METADATA_DB_USER,_METADATA_DB_PASSWORD,  _METADATA_DB_NAME):
    try:
        myDbConn = MongoClient(_METADATA_DB_SERVER,  int(_METADATA_DB_PORT), userName = _METADATA_DB_USER, authMechanism='SCRAM-SHA-1', password = _METADATA_DB_PASSWORD,  authSource = str(_METADATA_DB_NAME))
        return myDbConn
    except Exception as e:
        print("Error in opening Database Connection to Metadata!!" , e )
        print(traceback.print_stack())
        sys.exit()

def executeDBQuery(pDBConn, pSchema, pCollection, pQuery, pConditions):
        try:                                     
            myDb = pDBConn[pSchema]     
            myColl = myDb[pCollection]   
            myDoc = myColl.find(pQuery)
            return myDoc   
               
            
        except Exception as e:
            print("Error in executing Database Query!!",e)


def jsonExtractElement( obj, path):
    '''
    Extracts an element from a nested dictionary or
    a list of nested dictionaries along a specified path.
    If the input is a dictionary, a list is returned.
    If the input is a list of dictionary, a list of lists is returned.
    obj - list or dict - input dictionary or list of dictionaries
    path - list - list of strings that form the path to the desired element
    '''
    def extract(obj, path, ind, arr):
        '''
            Extracts an element from a nested dictionary
            along a specified path and returns a list.
            obj - dict - input dictionary
            path - list - list of strings that form the JSON path
            ind - int - starting index
            arr - list - output list
        '''
        key = path[ind]
        if ind + 1 < len(path):
            if isinstance(obj, dict):
                if key in obj.keys():
                    extract(obj.get(key), path, ind + 1, arr)
                else:
                    arr.append(None)
            elif isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        extract(item, path, ind, arr)
            else:
                arr.append(None)
        if ind + 1 == len(path):
            if isinstance(obj, list):
                if not obj:
                    arr.append(None)
                else:
                    for item in obj:
                        arr.append(item.get(key, None))
            elif isinstance(obj, dict):
                arr.append(obj.get(key, None))
            else:
                arr.append(None)
        return arr
    if isinstance(obj, dict):
        return extract(obj, path, 0, [])
    elif isinstance(obj, list):
        outer_arr = []
        for item in obj:
            outer_arr.append(extract(item, path, 0, []))
        return outer_arr
