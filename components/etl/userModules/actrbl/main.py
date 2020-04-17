#from pymongo import MongoClient
import os,sys,traceback
import json
from etl import ClsEtlSettings
from collections import OrderedDict 
import packages.utils.common 
from packages.utils.common import jsonExtractElement
#from pyspark import SparkContext, SparkConf
from packages.utils import etlUtils
#from pyspark.sql import SQLContext 
#from pyspark.sql import SparkSession
#from pyspark.sql.functions import lit, when, col, regexp_extract

import pandas as pd

class ClsAccountReceivables():
    _ACTRBL_DATA_MODEL = {}    
    _SITE_CODE = ""
    _ORG_CODE = ""
    _ENTITY_CODE = ""
    _MODULE_CODE = ""
    _DIV_CODE = ""
    _CATALOG_CODE = ""
    _DATASET_CODE = ""
    _DATAMODEL_CODE = ""
    _CATALOG_NAME = ""
    _DATEPARTITION_TYPE = ""
    _OBJECT_CODE = ""
    _DATASET_NAME = ""
    _DATAMODEL_NAME = ""    
    _DATA_SOURCE = []
    _DATA_TARGET = {}
    _OBJECT_ATTRIBUTES = OrderedDict()
    _PARTITION_KEYS = ""
    _PARTITION_DATEKEYS_DICT = {}
    _DIMENSIONS = OrderedDict()
    _AGGREGATES  = OrderedDict()
    _KPIS = OrderedDict()
    _MEASURES = OrderedDict()    
    _CONTAINERS = OrderedDict()

    _SPARK_SESSION = ""
    _HIVE_DB_NAME = ""
    _HIVE_BASE_TABLE_NAME = ""
    _DISPLAY_COLUMN_LIST = ""
    _SOURCE_COLUMN_LIST =  ""
    _PARTITION_COLUMNS_LIST = ""
    _DATE_COLUMNS_LIST = ""

    _COLUMNS_DC_SYSTEM = ""
    _COLUMNS_DC_CONSTANTS = ""
    _COLUMNS_DC_DATEKEYS = ""
    _COLUMNS_DC_FORMULA = ""
    _COLUMNS_DC_FUNCTION = ""
    
    _DF_DC_SYSTEM = ""
    _DF_DC_CONSTANTS = ""
    _DF_DC_DTKEYS = ""
    _DF_DC_FORMULA = ""
    _DF_DC_FUNCTION = ""
    _DF_PARTITION_KEYS = ""

    _DICT_ATTRIBUTES_DC_SYSTEM = OrderedDict()
    _DICT_ATTRIBUTES_DC_CONSTANT = OrderedDict()
    _DICT_ATTRIBUTES_DC_DATEKEYS = OrderedDict()
    _DICT_ATTRIBUTES_DC_FORMULA = OrderedDict()
    _DICT_ATTRIBUTES_DC_FUNCTION = OrderedDict()

    _SOURCE_DATA_RDD = ""
    _CALENDAR = []
    _SOURCE_COLUMNS = {}
    _DERIVED_COLUMNS = {}
    _CONSTANT_COLUMNS = {}
    _FLG_VALIDATE = ""
    _RDD_SOURCE = ""
    _ETL_PARAMS = ""
    

    def __init__(self, pSparkSession, pETLParams, pDataModel, pObjCode, pDataSet, pContainers, pAggregates, pKPIs, pCalendar):
        try:
            print('Initializing ETL for Account Receivables Module') 
            self._ACTRBL_DATA_MODEL = pDataModel
            self._ETL_PARAMS = pETLParams
            self._SITE_CODE = pETLParams._ETLEXEC_SITE_CODE
            self._ORG_CODE = pETLParams._ETLEXEC_ORG_CODE
            self._ENTITY_CODE = pETLParams._ETLEXEC_ENTITY_CODE
            self._MODULE_CODE = pETLParams._ETLEXEC_MODULE_CODE
            self._DIV_CODE =  pETLParams._ETLEXEC_DIV_CODE
            self._CATALOG_CODE = pDataModel["catalogCode"]
            self._DATASET = pDataSet
            self._DATA_SOURCE   = pDataSet["dataSource"]
            self._DATAMODEL_CODE =   pDataModel["dataModelCode"] 
            self._DATAMODEL_NAME =   pDataModel["dataModelName"] 
            self._OBJECT_CODE = pDataModel["objectName"]
            self._CALENDAR = pCalendar 
            self._CONTAINERS = pContainers 
            self._AGGREGATES = pAggregates
            self._KPIS = pKPIs
            self._OBJECT_CODE = pObjCode
            self._DF_OUTPUT = ""
            self._DATEPARTITION_TYPE = pDataModel["datePartitionKeys"]
            self._SPARK_SESSION = pSparkSession
            self._HIVE_DB_NAME = pETLParams._ETLEXEC_SITE_CODE + "_" + pETLParams._ETLEXEC_ORG_CODE + "_" + pETLParams._ETLEXEC_MODULE_CODE
            self._HIVE_BASE_TABLE_NAME = self._OBJECT_CODE
            #for key, attribute in p
            # Load active Target Storages setup for saving the datasets (tuple: _id & entire values as json)
            for  key, attributes in pDataSet.items():                
                if(key == "targetStorage"):
                    print("-> Loading Target Storage definitions....")
                    for attribute in attributes:
                        if attribute["isActive"] == "True":                            
                            self._DATA_TARGET[attribute["_id"]] = (attribute)
            for  key, attributes in pDataModel.items():                
                if(key == "objectAttributes"):
                    print("-> Loading Attributes....")
                    for attribute in attributes:     
                        if attribute["isIgnore"] =="False":
                            self._OBJECT_ATTRIBUTES[attribute["attributeName"]] = attribute["_id"]
                            if self._SOURCE_COLUMN_LIST == "":
                                self._SOURCE_COLUMN_LIST =  attribute["attributeName"]
                            else:
                                self._SOURCE_COLUMN_LIST = self._SOURCE_COLUMN_LIST  + "," + attribute["attributeName"]
                            if attribute["isVisible"] == "True":
                                if self._DISPLAY_COLUMN_LIST == "":
                                    self._DISPLAY_COLUMN_LIST = attribute["attributeName"]
                                else:
                                    self._DISPLAY_COLUMN_LIST = self._DISPLAY_COLUMN_LIST + "," + attribute["attributeName"]
                    if self._SOURCE_COLUMN_LIST =="" or self._DISPLAY_COLUMN_LIST =="" :
                        print("Error!!! System not able to create Source Columns. Please verify your data model definitions")
                        sys.exit()
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
                        
                            #Load column names as individual csv's
                            if k == "derivedBySystem":
                                self._DICT_ATTRIBUTES_DC_SYSTEM = v                                
                                for dc in v:                                                                                        
                                    if dc["isIgnore"] == "False":
                                        if self._COLUMNS_DC_SYSTEM == "" :
                                            self._COLUMNS_DC_SYSTEM = dc["attributeName"]
                                        else:
                                            self._COLUMNS_DC_SYSTEM = self._COLUMNS_DC_SYSTEM + "," +  dc["attributeName"]
                            elif k == "derivedByConstants":
                                self._DICT_ATTRIBUTES_DC_CONSTANT = v                                
                                for dc in v:                                                                                        
                                    if dc["isIgnore"] == "False":
                                        if self._COLUMNS_DC_CONSTANTS == "" :
                                            self._COLUMNS_DC_CONSTANTS = dc["attributeName"]
                                        else:
                                            self._COLUMNS_DC_CONSTANTS = self._COLUMNS_DC_CONSTANTS + "," +  dc["attributeName"]
                            elif k == "derivedByDateKeys":
                                self._DICT_ATTRIBUTES_DC_DATEKEYS = v
                                for dc in v:                                                                                        
                                    if dc["isIgnore"] == "False":
                                        if self._COLUMNS_DC_DATEKEYS == "" :
                                            self._COLUMNS_DC_DATEKEYS = dc["attributeName"]
                                        else:
                                            self._COLUMNS_DC_DATEKEYS = self._COLUMNS_DC_DATEKEYS +  "," + dc["attributeName"]
                            elif k == "derivedByFormula":
                                self._DICT_ATTRIBUTES_DC_FORMULA = v
                                for dc in v:                                                                                        
                                    if dc["isIgnore"] == "False":
                                        if self._COLUMNS_DC_FORMULA == "" :
                                            self._COLUMNS_DC_FORMULA = dc["attributeName"]
                                        else:
                                            self._COLUMNS_DC_FORMULA = self._COLUMNS_DC_FORMULA +  "," + dc["attributeName"]
                            elif k == "derivedByFunction":
                                self._DICT_ATTRIBUTES_DC_FUNCTION = v 
                                for dc in v:                                                                                        
                                    if dc["isIgnore"] == "False":
                                        if self._COLUMNS_DC_FUNCTION == "" :
                                            self._COLUMNS_DC_FUNCTION = dc["attributeName"]
                                        else:
                                            self._COLUMNS_DC_FUNCTION = self._COLUMNS_DC_FUNCTION +  "," + dc["attributeName"]
                            
                            for dc in v:                                                                                        
                                if dc["isIgnore"] == "False":
                                    self._DERIVED_COLUMNS[dc["attributeName"]] = dc
                                    
                
                #Loading all the partition keys defined for the data model as a dictionary.
                #Data will be partitioned based on these keys in (target storage - Parquet)
                elif(key == "partitionKeys"):
                    print("-> Loading Partition Keys..")
                    for attribute in attributes:                       
                        seq = attribute["seq"]
                        sPartitionKeys =""
                        if attribute["isActive"] == "True":
                            for key,val in attribute.items():                            
                                if key == "keys":                                    
                                    for i in val:
                                        sKey =  i["attributeName"]
                                        if i["derivedBy"] == "BySystem":                                            
                                            if i["isDateDimension"] == "True":
                                                lstDateKeys=[]
                                                lstDateKeys = i["dimGranularity"]
                                                sDateKeys = ""
                                                for x in range(0 , len(lstDateKeys)):                                            
                                                    if (sDateKeys == ""):
                                                        sDateKeys = sKey + "_" + str(lstDateKeys[x])
                                                    else:
                                                        sDateKeys = sDateKeys + "," + ( sKey + "_" + str(lstDateKeys[x]) )
                                               
                                                if sPartitionKeys == "":
                                                    sPartitionKeys = sDateKeys
                                                else:
                                                    sPartitionKeys = sPartitionKeys + "," + sDateKeys
                                                self._PARTITION_DATEKEYS_DICT[sKey] = sDateKeys
                                            else:
                                                if sPartitionKeys == "":
                                                    sPartitionKeys = sKey
                                                else:
                                                    sPartitionKeys = sPartitionKeys + "," + sKey
                                        elif i["derivedBy"] == "ByCustom":
                                            if i["isDateDimension"] == "True":
                                                lstDateKeys=[]
                                                lstDateKeys = i["dimGranularity"]
                                                sDateKeys = ""
                                                for x in range(0 , len(lstDateKeys)):                                            
                                                    if (sDateKeys == ""):
                                                        sDateKeys = sKey + "_" + str(lstDateKeys[x])
                                                    else:
                                                        sDateKeys = sDateKeys + "," + ( sKey + "_" + str(lstDateKeys[x]) )
                                               
                                                if sPartitionKeys == "":
                                                    sPartitionKeys = sDateKeys
                                                else:
                                                    sPartitionKeys = sPartitionKeys + "," + sDateKeys
                                                self._PARTITION_DATEKEYS_DICT[sKey] = sDateKeys
                                            else:
                                                if sPartitionKeys == "":
                                                    sPartitionKeys = sKey
                                                else:
                                                    sPartitionKeys = sPartitionKeys + "," + sKey                               
                                    
                                    # if sDateKeys!="":
                                    #     sPartitions = sKey + "," + ",".join(sDateKeys.split(","))
                                    # else:
                                    #     sPartitions = sKey

                                    print("-> Partition Keys:", sPartitionKeys)
                                
                            self._PARTITION_KEYS = sPartitionKeys 
                                             
                    print("-> Partition Keys:", sPartitionKeys)
                    
        except Exception as e:
            print("Error occurred initializing ETL for Account Receivables!!!" , e)

    def executeETLForAccountReceivables(self, pSparkSession,  pETLParams, pDataModel, pObjCode, pDictContainers, pAggregates, pKPIs):
        try:
            print("Loading Account Receivables Datasources..") 
            print("-> Reading Data Sources for Object:" ,self._OBJECT_CODE) 

             
            self._SOURCE_DATA_RDD =  etlUtils.importData(self, pSparkSession, self._DATA_SOURCE)         

            iRowCount = self._SOURCE_DATA_RDD.count()
            print("Total lines:", iRowCount)
            
            if iRowCount > 0:
                print("-> Validating Source Schema...")
                #if (etlUtils.validateSchema(pSparkSession, self._ACTRBL_DATA_MODEL, self._SOURCE_DATA_RDD)):
                if 1==1 :
                    #dfKeys = self._SOURCE_DATA_RDD.map(lambda x: (x[0],)).toDF(["Id"]) 
                    dfKeys = self._SOURCE_DATA_RDD.select("Id")

                    print("-> Generating Derived Columns based on System...")                    
                    self._DF_DC_SYSTEM = etlUtils.generateDCSystemDF(self, pSparkSession, dfKeys)
                    #print(self._DF_DC_SYSTEM.show())   

                    print("-> Generating Derived Columns based on Constants...")                    
                    self._DF_DC_CONSTANTS = etlUtils.generateDCConstantsDF(self, pSparkSession, dfKeys)
                    #print(self._DF_DC_CONSTANTS.show())                    
                   
                    print("-> Generating Derived Columns based on Formula...")
                    self._DF_DC_FORMULA =  etlUtils.generateDCFormulaDF (self, pSparkSession, dfKeys)
                    #print(self._DF_DC_FORMULA.show())

                    print("-> Generating Derived Columns based on Functions...")
                    self._DF_DC_FUNCTION =  etlUtils.generateDCFunctionDF (self, pSparkSession, dfKeys)
                    #print(self._DF_DC_FUNCTION.show())

                    print("-> Generating Derived Columns based on Date Keys...")
                    self._DF_DC_DTKEYS= etlUtils.generateDCDateKeysDF (self, pSparkSession, dfKeys)
                    #print(self._DF_DC_DTKEYS.show())

                    dfAllDCCols = dfKeys.join(self._DF_DC_SYSTEM,"Id", "outer" )
                    
                    if self._DF_DC_CONSTANTS is not None:
                        dfAllDCCols = dfAllDCCols.join(self._DF_DC_CONSTANTS, "Id", "outer")
                    if self._DF_DC_FORMULA is not None:
                        dfAllDCCols = dfAllDCCols.join(self._DF_DC_FORMULA, "Id", "outer")
                    if self._DF_DC_FUNCTION is not None:
                        dfAllDCCols = dfAllDCCols.join(self._DF_DC_FUNCTION, "Id", "outer")
                    if self._DF_DC_DTKEYS is not None:
                        dfAllDCCols = dfAllDCCols.join(self._DF_DC_DTKEYS, "Id", "outer")
                    
                    #sCols = self._SOURCE_COLUMN_LIST
                    
                    #myRddSource = self._SOURCE_DATA_RDD.map(lambda x:  x[1].split("\t"))
                    #df1 = myRddSource.toDF(sCols.split(","))

                    #df2 = self._SOURCE_DATA_RDD.map(lambda x:  (x[0], )).toDF(["Id"])
                    #dfSource = df2.crossJoin(df1)

                    if dfAllDCCols is not None:
                        dfFinal = dfAllDCCols.join(self._SOURCE_DATA_RDD,"Id", "inner")                    
                        
        

                    #self._DF_OUTPUT = etlUtils.generateDerivedColumns(self, pSparkSession, self._ACTRBL_DATA_MODEL, pETLParams, rddSourceData, "Test")
                    #print(dfFinal.show())       
                    if dfFinal !="" or dfFinal is not None:
                        print("-> Output successfully generated!!")  
                        etlUtils.saveData(self, dfFinal, self._DATA_TARGET , pDictContainers)   
                                     
                
            else:
                print("No data available for ingestion for the source defined!!", __name__)
                sys.exit()

            
        except Exception as e:
            print("Error occurred executing ETL for Account Receivables!!!" , e)
                  
           
            