#from pymongo  import Connection
from pymongo import MongoClient

from pprint import pprint
import json
import os, sys
import traceback
from packages.utils.common import openDBConnection

class ClsEtlExecParameters():
    _ETLEXEC_SITE_CODE=""
    _ETLEXEC_ORG_CODE=""
    _ETLEXEC_ENTITY_CODE=""
    _ETLEXEC_MODULE_CODE=""
    

    def __init__(self, pParamFile):
        try:
            with open(pParamFile, 'r') as fHandle:
                jsonData = json.load(fHandle)
                
            for x in jsonData:
                self._ETLEXEC_SITE_CODE = jsonData[x].get('siteCode')
                self._ETLEXEC_ORG_CODE = jsonData[x].get('organizationCode')
                self._ETLEXEC_ENTITY_CODE = jsonData[x].get('entityCode')
                self._ETLEXEC_MODULE_CODE = jsonData[x].get('moduleCode')
             
        except Exception as e:
            print("Error in reading ETL Execution Parameters from the file!!", e )
            print(traceback.print_stack())
            sys.exit()


class ClsEtlSettings():

    _METADATA_DB_CONN=""
    _METADATA_DB_TYPE=""
    _METADATA_DB_SERVER=""
    _METADATA_DB_NAME=""
    _METADATA_DB_USER=""
    _METADATA_DB_PASSWORD=""
    _METADATA_DB_PORT=""
    _METADATA_IS_SYSTEM=""
    _METADATA_ADMIN_SCHEMA=""
    _METADATA_SITE_SCHEMA = ""
    _METADATA_RECO_SCHEMA=""
    _METADATA_DEFAULT_SCHEMA = ""

    
    _ETL_APP_NAME = ""
    _ETL_APP_VERSION = "" 
    _ETL_APP_MODULES = ""    

    _LOG_FILE_NAME = ""
    _LOG_FILE_EXTN = ""
    _LOG_FOLDER_NAME = ""
    _LOG_FILE_NAME_DATE_FORMAT = ""
    _LOG_MAX_FILE_SIZE = ""
    _LOG_ROTATE_DAILY = ""
    _LOG_BACKUP_COUNT = ""
    _LOG_TEXT_FORMATTER = ""
    _LOG_TEXT_DATE_FORMATTER = ""
    
    
    def __init__(self):
        try:
            sFile = "config\\settings.cfg"
            with open(sFile,'r') as fHandle:
                jsonData = json.load(fHandle)             
            for x in jsonData:                
                if x == "metadataDb":                   
                    self._METADATA_DB_SERVER =  jsonData[x].get('dbServer')
                    self._METADATA_DB_TYPE = jsonData[x].get('dbType')
                    self._METADATA_DB_PORT = jsonData[x].get('dbPort')
                    self._METADATA_DB_USER = jsonData[x].get('dbUser')
                    self._METADATA_DB_PASSWORD = jsonData[x].get('dbPassword')
                    self._METADATA_DB_NAME = jsonData[x].get('dbName')
                    self._METADATA_DEFAULT_SCHEMA = jsonData[x].get('defaultSchema')
                    self._METADATA_IS_SYSTEM = jsonData[x].get('isSystem')           
                    print('Loaded ETL Settings successfully!!!')

                    self._METADATA_DB_CONN = MongoClient(self._METADATA_DB_SERVER,  int(self._METADATA_DB_PORT), userName = self._METADATA_DB_USER, authMechanism='SCRAM-SHA-1', password = self._METADATA_DB_PASSWORD,  authSource = str(self._METADATA_DB_NAME), maxPoolSize=10, waitQueueTimeoutMS=100)                 
                    print('Connected to Metadata Database successfully!!!')
                    
                #else:
                #    print("Settings missing for reading metadata!! No details specified for Metadata Database" )
             
        except (FileNotFoundError, IOError):
            print("Error in loadEtlSettings!! Settings file not found!!")
            sys.exit()
        except Exception as e:            
            print("Error in Loading ETL Settings!!" , e )
            print(traceback.print_stack())
            sys.exit()


    
    #To Do
    def verifyETLSettings(self):
        try:
            #Check if ETL Parameters are configured correctly. Compare the given Parameters to the ones configured in the system
            print('ETL Settings verified successfully!!')
            return 'True'
        except Exception as e:
            print("Error in verifying ETL Settings" ,e)

