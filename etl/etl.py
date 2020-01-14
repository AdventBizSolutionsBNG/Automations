#from pymongo  import Connection
from pymongo import MongoClient

from pprint import pprint
import json
import os, sys
import traceback
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

#from pyspark.sql import sparkSession

from packages.utils.common import openDBConnection

class ClsEtlExecParameters():
    _ETLEXEC_SITE_CODE=""
    _ETLEXEC_ORG_CODE=""
    _ETLEXEC_ENTITY_CODE=""
    _ETLEXEC_MODULE_CODE=""
    _ETLEXEC_CALENDAR = ""
  
    

    def __init__(self, pParamFile):
        try:
            with open(pParamFile, 'r') as fHandle:
                jsonData = json.load(fHandle)
                
            for x in jsonData:
                self._ETLEXEC_SITE_CODE = jsonData[x].get('siteCode')
                self._ETLEXEC_ORG_CODE = jsonData[x].get('organizationCode')
                self._ETLEXEC_ENTITY_CODE = jsonData[x].get('entityCode')
                self._ETLEXEC_MODULE_CODE = jsonData[x].get('moduleCode')
                self._ETLEXEC_CALENDAR = jsonData[x].get('calendar')
                
             
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
    
    _ETLSPARK_SETTINGS = ""
    _ETLSPARK_CONTEXT = ""
    _ETLSPARK_SESSION = ""
    
    def __init__(self):
        try:
            sFile = "config\\settings.cfg"
            with open(sFile,'r') as fHandle:
                settings = json.load(fHandle)   
                      
            for settingKey, settingValue in settings.items():                            
                if settingKey == "metadataDb":                                       
                    self._METADATA_DB_SERVER =  settingValue['dbServer']
                    self._METADATA_DB_TYPE = settingValue['dbType']
                    self._METADATA_DB_PORT = settingValue['dbPort']
                    self._METADATA_DB_USER = settingValue['dbUser']
                    self._METADATA_DB_PASSWORD = settingValue['dbPassword']
                    self._METADATA_DB_NAME = settingValue['dbName']
                    self._METADATA_DEFAULT_SCHEMA = settingValue['defaultSchema']
                    self._METADATA_IS_SYSTEM = settingValue['isSystem']
                     
                elif settingKey == "sparkEngine":
                    self._ETLSPARK_SETTINGS = settingValue
                    self._ETLSPARK_CONTEXT = settingValue['sparkContext']                    
                    self._ETLSPARK_SESSION = settingValue['sparkSession']
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


    
    def startSparkSession(self):
        try:
            pass

        except Exception as e:
            print("Error in starting Spark Session", e)

    #To Do
    def verifyETLSettings(self):
        try:
            #Check if ETL Parameters are configured correctly. Compare the given Parameters to the ones configured in the system
            print('ETL Settings verified successfully!!')
            return 'True'
        except Exception as e:
            print("Error in verifying ETL Settings" ,e)

    def startSparkContext(self):
        try:
            print("Initializing Spark Context....")
            confCxt = SparkConf() \
                        .setAppName(self._ETLSPARK_SETTINGS["appName"]) \
                        .setMaster(self._ETLSPARK_SETTINGS["hostName"]) \
                        .set("spark.executor.memory", self._ETLSPARK_CONTEXT["spark.executor.memory"]) \
                        .set("spark.driver.cores", self._ETLSPARK_CONTEXT["spark.driver.cores"]) \
                        .set("spark.logConf", self._ETLSPARK_CONTEXT["spark.logConf"]) \
                        .set("spark.eventLog.enabled", self._ETLSPARK_CONTEXT["spark.eventLog.enabled"]) \
                        .set("spark.cores.max", self._ETLSPARK_CONTEXT["spark.cores.max"]) \
                        .set("spark.executor.cores", self._ETLSPARK_CONTEXT["spark.executor.cores"]) 

            #spark = SparkSession
            spark = SparkSession.builder.config(conf=confCxt).getOrCreate()
            #sc = SparkContext(conf = confCxt).getOrCreate
            sc = spark.sparkContext
            
            return sc
            
            # spark = SparkSession \
            #             .builder.appName(self._ETLSPARK_SETTINGS["appName"])  \
            #             .master(self._ETLSPARK_SETTINGS["hostName"]).getOrCreate()  \
            #             .config("spark.executor.memory", self._ETLSPARK_CONTEXT["spark.executor.memory"]) \
            #             .getOrCreate()    
                        
            #sc = spark.sparkContext
            
            
            #print(sc.getConf().getAll())
            

        except Exception as e:
            print("Error in initializing Spark Context", e)
            print(traceback.print_stack())
            sys.exit()
    

