from pymongo import MongoClient
import os,sys,traceback
import json
from etl import ClsEtlSettings
from collections import OrderedDict 
import packages.utils.common 
from packages.utils.common import jsonExtractElement
from pyspark import SparkContext, SparkConf
from packages.utils import etlUtils
from pyspark.sql import SQLContext 
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, when, col, regexp_extract

import pandas as pd

class ClsAccountReceivables():
    _ACTRBL_DATA_MODEL = {}    
    _SITE_CODE = ""
    _ORG_CODE = ""
    _CATALOG_CODE = ""
    _DATASET_CODE = ""
    _DATAMODEL_CODE = ""
    _CATALOG_NAME = ""
    _OBJECT_NAME = ""
    _DATASET_NAME = ""
    _DATAMODEL_NAME = ""    
    _DATA_SOURCE = []
    _DATA_TARGET = {}
    _OBJECT_ATTRIBUTES = OrderedDict()
    _PARTITION_KEYS = OrderedDict()
    _DIMENSIONS = OrderedDict()
    _AGGREGATES  = OrderedDict()
    _MEASURES = OrderedDict()    
    _CONTAINERS = OrderedDict()
    _CALENDAR = []
    _SOURCE_COLUMNS = {}
    _DERIVED_COLUMNS = {}
    _CONSTANT_COLUMNS = {}
    _FLG_VALIDATE = ""
    _RDD_SOURCE = ""
    _ETL_PARAMS = ""
    

    def __init__(self, pSparkContext, pDoc, pETLParams, pDataSet, pCalendar):
        try:
            print('Initializing ETL for Account Receivables Module') 
            self._ACTRBL_DATA_MODEL = pDoc
            self._ETL_PARAMS = pETLParams
            self._SITE_CODE = pETLParams._ETLEXEC_SITE_CODE
            self._ORG_CODE = pETLParams._ETLEXEC_ORG_CODE
            self._CATALOG_CODE = pDoc["catalogCode"]
            self._DATA_SOURCE   = pDataSet["dataSource"]
            self._DATAMODEL_CODE =   pDoc["dataModelCode"] 
            self._DATAMODEL_NAME =   pDoc["dataModelName"] 
            self._OBJECT_NAME = pDoc["objectName"]
            self._CALENDAR = pCalendar  
            self._DF_OUTPUT = ""

            # Load active Target Storages setup for saving the datasets (tuple: _id & entire values as json)
            for  key, attributes in pDataSet.items():
                if(key == "targetStorage"):
                    print("-> Loading Target Storage definitions....")
                    for attribute in attributes:
                        if attribute["isActive"] == "True":                            
                            self._DATA_TARGET[attribute["_id"]] = (attribute)
            for  key, attributes in pDoc.items():
                if(key == "objectAttributes"):
                    print("-> Loading Attributes....")
                    for attribute in attributes:                                           
                        self._OBJECT_ATTRIBUTES[attribute["attributeName"]] = attribute["_id"]
                elif(key == "dimensions"):
                    print("-> Loading Dimensions....")
                    for attribute in attributes:                        
                        for k,v in attribute.items():                            
                            for dimension in v:                                
                                if dimension["isActive"] == "True":
                                    self._DIMENSIONS[dimension["dimCode"]] = dimension 
                elif(key == "measures"):
                    print("-> Loading Measures....")
                    for measure in attributes:                        
                        if (measure["isActive"]) == "True":
                            self._MEASURES[measure["measureCode"]] = measure
                elif(key == "derivedColumns"):
                    print("-> Loading Derived Columns....")
                    for attribute in attributes:                        
                        for k,v in attribute.items():                            
                            for dc in v:                                                             
                                if dc["isIgnore"] == "False":
                                    self._DERIVED_COLUMNS[dc["attributeName"]] = dc
                
                #Loading all the partition keys defined for the data model as a dictionary.
                #Data will be partitioned based on these keys in (target storage - Parquet)
                elif(key == "partitionKeys"):
                    print("-> Loading Partition Keys..")
                    sPartitions = ""
                    for keys in v:
                        seq = keys["seq"]
                        sKeys=""
                        for key,val in keys.items():                            
                            if key == "keys":
                                for i in val:                                    
                                    if i["isDateDimension"] == "True":
                                        lstDateKeys=[]
                                        lstDateKeys = i["dimGranularity"]
                                        sDateKeys = ""
                                        for x in range(0 , len(lstDateKeys)):                                            
                                            if (sDateKeys == ""):
                                                sDateKeys = str(lstDateKeys[x])
                                            else:
                                                sDateKeys = sDateKeys + "," + str(lstDateKeys[x])

                                    if sKeys =="":
                                        if i["derivedBy"] == "constants":
                                            sKeys =  i["attributeName"]                                        
                                    else:
                                        if i["derivedBy"] == "constants":
                                            sKeys= sKeys + "," +  i["attributeName"]                                 
                                
                                if sDateKeys!="":
                                    sPartitions = sKeys + "," + ",".join(sDateKeys.split(","))
                                else:
                                    sPartitions = sKeys

                                print("->Partition Keys:", sPartitions)
                                
                        self._PARTITION_KEYS[seq] = sPartitions  

        except Exception as e:
            print("Error occurred initializing ETL for Account Receivables!!!" , e)

    def executeETLForAccountReceivables(self, pSparkContext, pDoc, pETLParams, pDataSet):
        try:
            print("Loading Account Receivables Datasources..") 
            print("-> Reading Data Sources for Object:" ,self._OBJECT_NAME)            
            #spark = SparkSession(sc)
            rddSourceData = etlUtils.importData(pSparkContext, self._DATA_SOURCE)
            iRowCount = rddSourceData.count()
            #print("Total lines:", iRowCount)
            if iRowCount > 0:
                print("-> Validating Source Schema...")
                if (etlUtils.validateSchema(pSparkContext, self._ACTRBL_DATA_MODEL, rddSourceData)):
                    print("-> Generating Derived Columns...")
                    self._DF_OUTPUT = etlUtils.generateDerivedColumns(self, pSparkContext, self._ACTRBL_DATA_MODEL,pETLParams, rddSourceData, "Test")
                    if self._DF_OUTPUT !="" or self._DF_OUTPUT is not None:
                        print("-> Outut successfully generated!! Saving Datasets now...")  
                        etlUtils.saveData(self, self._DF_OUTPUT,self._DATA_TARGET)                  
                
            else:
                print("No data available for ingestion for the source defined!!", __name__)
                sys.exit()

            
        except Exception as e:
            print("Error occurred executing ETL for Account Receivables!!!" , e)
                  
           
            