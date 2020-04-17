#from pymongo  import Connection

from pymongo import MongoClient
from pyhive import hive
#from pprint import pprint
import json
import os, sys
import traceback
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession,SQLContext

#from pyspark.sql import sparkSession

#from packages.utils.common import openDBConnection
import coreEngine.commonUtils as utils

class ClsEtlExecParameters():
    _ETLEXEC_SITE_CODE=""
    _ETLEXEC_ORG_CODE=""
    _ETLEXEC_ENTITY_CODE=""
    _ETLEXEC_MODULE_CODE=""
    _ETLEXEC_CALENDAR = ""
    _ETLEXEC_DIV_CODE = ""
    _FLG_PROCESS_AGGREGATES = ""
    _FLG_PROCESS_CONTAINERS = ""
    _FLG_PROCESS_KPIS = ""
    _FLG_PROCESS_INPUT_DATA = ""
    _FLG_VALIDATE_SCHEMA = ""

  
    

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

                self._FLG_PROCESS_AGGREGATES = jsonData[x].get('processAggregates')
                self._FLG_PROCESS_CONTAINERS = jsonData[x].get('processContainers')
                self._FLG_PROCESS_INPUT_DATA = jsonData[x].get('processInputData')
                self._FLG_PROCESS_KPIS = jsonData[x].get('processKPIs')
                self._FLG_VALIDATE_SCHEMA = jsonData[x].get('validateSchema')

                if self._ETLEXEC_MODULE_CODE == "ACTRBL":
                    self._ETLEXEC_DIV_CODE = jsonData[x].get('divCode')
                
             
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

    _TX_DB_TYPE = ""
    _TX_DB_SERVER = ""
    _TX_DB_PORT = ""
    _TX_DB_USER = ""
    _TX_DB_PASSWD = ""
    _TX_IS_IMPERSONATED = ""
    _TX_DB_CONN = ""
    _TX_DB_NAME = ""


    def __init__(self, pETLParameters):
        try:
            sFile = "config//settings.cfg"
            with open(sFile,'r') as fHandle:
                settings = json.load(fHandle)   
                      
            for settingKey, settingValue in settings.items():                            
                if settingKey == "metadataDb":   
                    if  settingValue['dbType'] == "mongo":
                        self._METADATA_DB_SERVER =  settingValue['dbServer']
                        self._METADATA_DB_TYPE = settingValue['dbType']
                        self._METADATA_DB_PORT = settingValue['dbPort']
                        self._METADATA_DB_USER = settingValue['dbUser']
                        self._METADATA_DB_PASSWORD = settingValue['dbPassword']
                        self._METADATA_DB_NAME = settingValue['dbName']
                        self._METADATA_DEFAULT_SCHEMA = settingValue['defaultSchema']
                        self._METADATA_IS_SYSTEM = settingValue['isSystem']
                    else:
                        print("Error!! Incorrect Metadata Database Type specified!! Verify your ETL Settings!!")
                        sys.exit()
                     
                elif settingKey == "processingEngine":
                    if settingValue['engineType'] == "sparkEngine":
                        self._ETLSPARK_SETTINGS = settingValue
                        self._ETLSPARK_CONTEXT = settingValue['sparkContext']                         
                    else:
                        print("Error!! Incorrect Processing Engine Type specified!! Verify your ETL Settings!!")
                        sys.exit()

                elif settingKey == "transactionDb":
                    if settingValue['dbType'] == "hive":
                        self._TX_DB_TYPE = settingValue['dbType']
                        self._TX_DB_SERVER = settingValue['dbServer']
                        self._TX_DB_PORT = settingValue['dbPort']
                        self._TX_IS_IMPERSONATED = settingValue['isImpersonated']
                        if self._TX_IS_IMPERSONATED:
                            self._TX_DB_USER = ""
                            self._TX_DB_PASSWD = ""
                        else:
                            self._TX_DB_USER = settingValue['dbUser']
                            self._TX_DB_PASSWD = settingValue['dbPassword']                        
                    else:
                        print("Error!! Incorrect Transaction Database Type specified!! Verify your ETL Settings!!")
                        sys.exit()

            
            print("Connecting to Metadata Database....")
            self._METADATA_DB_CONN = MongoClient(self._METADATA_DB_SERVER,  int(self._METADATA_DB_PORT), userName = self._METADATA_DB_USER, authMechanism='SCRAM-SHA-1', password = self._METADATA_DB_PASSWORD,  authSource = str(self._METADATA_DB_NAME), maxPoolSize=10, waitQueueTimeoutMS=100)                 
            print(' Connected to Metadata Database successfully!!!')
            
            
            print("Connecting to Transaction Database....")
            sDBName = pETLParameters._ETLEXEC_SITE_CODE + "_" + pETLParameters._ETLEXEC_ORG_CODE + "_" + pETLParameters._ETLEXEC_MODULE_CODE
            self._TX_DB_NAME = sDBName
            print(" -> DB Name:",sDBName)
            if (self._TX_IS_IMPERSONATED):
                self._TX_DB_CONN = hive.connect(host= self._TX_DB_SERVER, port= self._TX_DB_PORT, auth="NONE",  database=sDBName).cursor()
            else:
                self._TX_DB_CONN = hive.connect(host= self._TX_DB_SERVER, port= self._TX_DB_PORT, auth="NONE", username=self._TX_DB_USER, password= self._TX_DB_PASSWD, database=sDBName).cursor()
            # self._TX_DB_CONN.execute("select * from st001_org001_actrbl.sample_ext_partition_2")
            # print (self._TX_DB_CONN.fetchall())
            

            print(' Connected to Transaction Database successfully!!!')  
            print('Loaded ETL Settings successfully!!!')

        except (FileNotFoundError, IOError):
            print("Error in loading ETL Settings!! Settings file not found!!")
            sys.exit()
        except Exception as e:            
            print("Error in Loading ETL Settings!! Verify your ETL Settings in settings.cfg file!!" , e )
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
            #print("-->",self._ETLSPARK_CONTEXT["hive.metastore.uri"])
            sSQLWarehouseDir = self._ETLSPARK_CONTEXT["spark.sql.warehouse.dir"] + "/" + self._TX_DB_NAME + ".db"
            confCxt = SparkConf() \
                        .setAppName(self._ETLSPARK_SETTINGS["appName"]) \
                        .setMaster(self._ETLSPARK_SETTINGS["hostName"]) \
                        .set("spark.executor.memory", self._ETLSPARK_CONTEXT["spark.executor.memory"]) \
                        .set("spark.driver.cores", self._ETLSPARK_CONTEXT["spark.driver.cores"]) \
                        .set("spark.logConf", self._ETLSPARK_CONTEXT["spark.logConf"]) \
                        .set("spark.eventLog.enabled", self._ETLSPARK_CONTEXT["spark.eventLog.enabled"]) \
                        .set("spark.cores.max", self._ETLSPARK_CONTEXT["spark.cores.max"]) \
                        .set("spark.executor.cores", self._ETLSPARK_CONTEXT["spark.executor.cores"]) \
                        .set("spark.dynamicAllocation.enabled", "true") \
                        .set("spark.sql.legacy.allowCreatingManagedTableUsingNonemptyLocation", "true") \
                        .set("spark.sql.warehouse.dir", sSQLWarehouseDir) \
                        .set("spark.hadoop.dfs.client.use.datanode.hostname", "true")
                        
            #spark = SparkSession
            mySpark = SparkSession.builder.config(conf=confCxt).config("hive.exec.dynamic.partition.mode", "nonstrict").config("hive.exec.dynamic.partition" , "true").enableHiveSupport().getOrCreate()
            #sc = SparkContext(conf = confCxt).getOrCreate
            sc = mySpark.sparkContext
            
            SparkContext.setSystemProperty("hive.metastore.uris", self._ETLSPARK_CONTEXT["hive.metastore.uris"])

            sqlContext = SQLContext(sc)
            sSettings = mySpark.sparkContext._conf.getAll()
            print ("-> Spark Settings:")
            for item in sSettings: 
                print(item)

            return sqlContext
            
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
    

