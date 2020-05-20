#from pymongo import MongoClient
import os,sys,traceback
import json
from coreEngine.setup import ClsEtlSettings
from collections import OrderedDict 
#import packages.utils.common 
#from packages.utils.common import jsonExtractElement
#from pyspark import SparkContext, SparkConf
#from packages.utils import etlUtils
#from pyspark.sql import SQLContext 
#from pyspark.sql import SparkSession
#from pyspark.sql.functions import lit, when, col, regexp_extract
import os,sys,traceback
import json
from datetime import datetime, date
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import uuid
from pyspark.sql.functions import *
from pyspark.sql.functions import lit, when, col, regexp_extract , udf
from pyspark.sql.functions import year, month, quarter, weekofyear, dayofyear, dayofweek, dayofmonth
from pyspark.sql.types import DateType
from dateutil.relativedelta import relativedelta

import pandas as pd

class ClsCommonModule():
    _SOURCE_DATA_MODEL = {}    
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
    _DICT_TARGET_STORAGE = {}
    _OBJECT_ATTRIBUTES = OrderedDict()
    _PARTITION_KEYS = ""
    _PARTITION_DATEKEYS_DICT = {}
    _DIMENSIONS = OrderedDict()
    _DICT_AGGREGATES  = OrderedDict()
    _DICT_KPIS = OrderedDict()
    _DICT_MEASURES = OrderedDict()    
    _DICT_CONTAINERS = OrderedDict()

    _SPARK_SESSION = ""
    _TX_DB_CONN = ""
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

    _SOURCE_DATA_DF = ""
    _CALENDAR = []
    _SOURCE_COLUMNS = {}
    _DERIVED_COLUMNS = {}
    _CONSTANT_COLUMNS = {}
    _FLG_VALIDATE = ""
    _RDD_SOURCE = ""
    _ETL_PARAMS = ""
    

    def __init__(self, pSparkSession, pModuleCode, pETLParams, pTXDBConn, pDataModel, pObjCode, pDataSet, pContainers, pAggregates, pKPIs, pCalendar):
        try:
            print('Initializing ETL .....') 
            self._SOURCE_DATA_MODEL = pDataModel
            self._ETL_PARAMS = pETLParams
            self._SITE_CODE = pETLParams._ETLEXEC_SITE_CODE
            self._ORG_CODE = pETLParams._ETLEXEC_ORG_CODE
            self._ENTITY_CODE = pETLParams._ETLEXEC_ENTITY_CODE
            self._MODULE_CODE = pModuleCode
            self._DIV_CODE =  pETLParams._ETLEXEC_DIV_CODE
            self._CATALOG_CODE = pDataModel["catalogCode"]
            self._DATASET = pDataSet
            self._DATA_SOURCE   = pDataSet["dataSource"]
            self._DATAMODEL_CODE =   pDataModel["dataModelCode"] 
            self._DATAMODEL_NAME =   pDataModel["dataModelName"] 
            self._OBJECT_CODE = pDataModel["objectName"]
            self._CALENDAR = pCalendar 
            self._DICT_CONTAINERS = pContainers 
            self._DICT_AGGREGATES = pAggregates
            self._DICT_KPIS = pKPIs
            self._OBJECT_CODE = pObjCode
            self._DF_OUTPUT = ""
            self._DATEPARTITION_TYPE = pDataModel["datePartitionModel"]
            self._SPARK_SESSION = pSparkSession
            self._TX_DB_CONN = pTXDBConn
            self._HIVE_DB_NAME = pETLParams._ETLEXEC_SITE_CODE + "_" + pETLParams._ETLEXEC_ORG_CODE + "_" + pETLParams._ETLEXEC_MODULE_CODE
            self._HIVE_BASE_TABLE_NAME = self._OBJECT_CODE
             
            # Load active Target Storages setup for saving the datasets (tuple: _id & entire values as json)
            for  k, a in pDataSet.items():                
                if(k == "targetStorage"):
                    print("-> Loading Target Storage definitions....")
                    for attribute in a:
                        if attribute["isActive"] == "True":                            
                            self._DICT_TARGET_STORAGE[attribute["_id"]] = (attribute)
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
                            self._DICT_MEASURES[measure["measureCode"]] = measure
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
            print("Error occurred initializing ETL!!!" , e)

    #def executeETL(self, pSparkSession,  pETLParams, pDataModel, pObjCode, self._DICT_CONTAINERS, pAggregates, pKPIs):
    def executeETL(self):
        try:
            print("Loading Datasources..") 
            print("-> Reading Data Sources for Object:" ,self._OBJECT_CODE) 

             
            self._SOURCE_DATA_DF =  self.importData()         

            iRowCount = self._SOURCE_DATA_DF.count()
            #iRowCount = 1000
            print("Total lines:", iRowCount)
            
            if iRowCount > 0:
                print("Validating Source Schema...")
                #if (self.validateSchema())   #self._SPARK_SESSION, self._SOURCE_DATA_MODEL, self._SOURCE_DATA_DF)):
                if 1==1 :
                    #dfKeys = self._SOURCE_DATA_DF.map(lambda x: (x[0],)).toDF(["Id"]) 
                    dfKeys = self._SOURCE_DATA_DF.select("Id")

                    print("-> Generating Derived Columns based on System...")                    
                    self._DF_DC_SYSTEM = self.generateDCSystemDF( dfKeys)
                    #print(self._DF_DC_SYSTEM.show())   

                    print("-> Generating Derived Columns based on Constants...")                    
                    self._DF_DC_CONSTANTS = self.generateDCConstantsDF( dfKeys)
                    #print(self._DF_DC_CONSTANTS.show())                    
                   
                    print("-> Generating Derived Columns based on Formula...")
                    self._DF_DC_FORMULA =  self.generateDCFormulaDF ( dfKeys)
                    #print(self._DF_DC_FORMULA.show())

                    print("-> Generating Derived Columns based on Functions...")
                    self._DF_DC_FUNCTION =  self.generateDCFunctionDF ( dfKeys)
                    #print(self._DF_DC_FUNCTION.show())

                    print("-> Generating Derived Columns based on Date Keys...")
                    self._DF_DC_DTKEYS= self.generateDCDateKeysDF ( dfKeys)
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
                    
                    #myRddSource = self._SOURCE_DATA_DF.map(lambda x:  x[1].split("\t"))
                    #df1 = myRddSource.toDF(sCols.split(","))

                    #df2 = self._SOURCE_DATA_DF.map(lambda x:  (x[0], )).toDF(["Id"])
                    #dfSource = df2.crossJoin(df1)

                    if dfAllDCCols is not None:
                        dfFinal = dfAllDCCols.join(self._SOURCE_DATA_DF,"Id", "inner")            

                    #self._DF_OUTPUT = self.generateDerivedColumns(self, self._SPARK_SESSION, self._SOURCE_DATA_MODEL, pETLParams, rddSourceData, "Test")
                    #print(dfFinal.show())       
                    if dfFinal !="" or dfFinal is not None:
                        print("-> Output successfully generated!!")  
                        self.saveData(dfFinal)   
                                     
                
            else:
                print("No data available for ingestion for the source defined!!", __name__)
                sys.exit()

            
        except Exception as e:
            print("Error occurred executing ETL!!!" , e)
                  
           

    def importData(self):
        try:           
            print("**************** Importing Data ****************")
            for dataSource in self._DATA_SOURCE:
                if dataSource['storageType'] == "FILE":                   
                    if dataSource['folderPathPattern'] == "" or dataSource['folderPathPattern'] is None:                        
                        if dataSource['fileNamePattern'] =="" or   dataSource['fileNamePattern']  is None:                          
                            sSourceFile = dataSource['folderPath'] + "/" + dataSource['fileName']  + "." +  dataSource['fileExtn']                              
                            if os.path.isfile(sSourceFile):
                                if(dataSource['isZipped']) == 'False':
                                    if(dataSource['isPassword']) == 'False' or (dataSource['isPassword']) == "":                                        
                                        sSeparator = dataSource['separator']
                                        if (sSeparator == "\t" or sSeparator == ","):  
                                            print(" -> Reading Source File:", sSourceFile)                                           
                                            iSkipRows = int(dataSource['startRow'])
                                            if dataSource['endRow'] !="" and dataSource['endRow'] is not None:
                                                iEndRows = int(dataSource['endRow'])
                                            else:
                                                iEndRows = 0
                                            sColNames = ""
                                        
                                            # generating a unique batch Id and adding to the rdd   
                                            # TODO : save batch status to a table          
                                            batchId = str(self.generateNewBatchId())

                                            #print("Columns:", self._SOURCE_DATA_MODEL._SOURCE_COLUMN_LIST )
                                            #sc = SparkContext("local","readSource")
                                            if iSkipRows >= 0:
                                                if iEndRows > 0:
                                                    #rddSourceData = self._SPARK_SESSION.textFile(sSourceFile).zipWithIndex().filter(lambda x: x[1] >=iSkipRows).filter(lambda y: y[1] <= iEndRows)
                                                    df = self._SPARK_SESSION.read.csv(sSourceFile, header = True , sep = "\\t" , inferSchema = True )
                                                    df = df.withColumn("Id", monotonically_increasing_id())
                                                elif iEndRows==0:
                                                    #rddSourceData = self._SPARK_SESSION.textFile(sSourceFile).zipWithIndex().filter(lambda x: x[1] >=iSkipRows)
                                                    df = self._SPARK_SESSION.read.csv(sSourceFile, header = True ,  sep = "\\t" , inferSchema = True  )
                                                    df = df.withColumn("Id", monotonically_increasing_id())
                                                else:
                                                    pass                                               
                                            else:
                                                pass
                                         
                                            print(" -> Total Rows:", df.count())
                                            print(" -> Reference Batch Id:",batchId )
                                            df = df.withColumn("batchId", lit(batchId) )                                        
                                            return df
                                        else:
                                            print("*** TO DO *** OTHER SEPARATORS")
                                    else:
                                        print('*** TO DO *** USE PASSWORD TO OPEN THE FILE AND INGEST')
                                else:
                                    print("*** TO DO *** UNZIP FILE AND INGEST")
                                
                            else:
                                print("Error locating source file. Please verify the filename and the location in the config. Location:", sSourceFile)
                        else:
                            print("*** TO DO *** USE REGEX TO DECODE THE FILE NAME PATTERN ")                

        except Exception as e:
            print("Error in importing data for the Source!!", __name__, " Error->", e)
            print(traceback.print_stack())


    def validateSchema(self):
        try:
            # attributes = []
            # seq = 0
            # for key in pDictDataModel.items():   
            #     #print("-->",key)                  
            #     attributes.append((key,seq))
            #     seq += 1
            return "True"
            for  key, attributes in self._SOURCE_DATA_MODEL.items():
                if(key =="objectAttributes"):    
                    iColPos = 0                
                    for attribute in attributes:                        
                        if attribute["isValidateData"] == "True":
                            print("--> Validating Schema for attribute:",attribute["attributeName"], " --> Attribute Data Type:", attribute["attributeDataType"] , "--> ColPosition:", (iColPos))
                            if attribute["attributeDataType"] == "string":
                                if attribute["isRequired"]=="True":
                                    check_string = self._SOURCE_DATA_DF.map \
                                        (
                                            lambda x : "True" if str(type(x.split("\t")[iColPos])) == "<type 'unicode'>" and len(x.split("\t")[iColPos]) > 0 else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_string.take(check_string.count())) != 0:
                                        print("Error!!! Schema Validation Failed.DataType String expected for Attribute:", attribute["attributeName"])
                                # elif attribute["isRequired"]=="False":
                                #     check_string = self._SOURCE_DATA_DF.map \
                                #             (
                                #                 lambda x: "True" if len(x.split("\t")[iColPos]) == 0 or str(type(x.split("\t")[iColPos])) == "<type 'unicode'>" else "False"
                                #             ).filter \
                                #             (
                                #                 lambda x: x == "False"
                                #             )
                                #     if len(check_string.take(check_string.count())) != 0:
                                #         print("Wrong Data Found in check_string else condition")

                            # check for property integer
                            if attribute["attributeDataType"] == "integer":
                                if attribute["isRequired"] == "True":
                                    print(" Checking for Integer Data Type:")
                                    numbers = set([str(num) for num in range(0,10)])
                                    check_integer = self._SOURCE_DATA_DF.map \
                                        (
                                            lambda x : "True" if len(set([num for num in x.split("\t")[iColPos]]).difference(numbers)) == 0 and len(x.split("\t")[iColPos]) > 0 else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_integer.take(check_integer.count())) != 0:
                                        print("Error!!! Schema Validation Failed.DataType Integer expected for Attribute:", attribute["attributeName"])
                                        
                                # elif attribute["isRequired"] == "False":
                                #     numbers = set([str(num) for num in range(0, 10)])
                                #     check_integer = self._SOURCE_DATA_DF.map \
                                #         (
                                #             lambda x: "True" if len(set([num for num in x.split("\t")[iColPos]]).difference(numbers)) == 0 and len(x.split("\t")[iColPos]) > 0 else "False"
                                #         ).filter \
                                #         (
                                #             lambda x: x == "False"
                                #         )
                                #     if len(check_integer.take(check_integer.count())) != 0:
                                #         print("Wrong Data Found in check_integer else condition")
                            
                            # check for property attributeMaxLength
                            if int(attribute["attributeMaxLength"]) > 0:
                                if attribute["isRequired"] == "True":
                                    print(" Checking for Max Length Data Type:")
                                    maxLength = int(attribute["attributeMaxLength"])
                                    check_length = self._SOURCE_DATA_DF.map \
                                        (
                                            lambda x : "True" if len(x.split("\t")[iColPos]) == 0 and len(x.split("\t")[iColPos]) <= maxLength else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_length.take(check_length.count())) != 0:
                                        print("Error!!! Schema Validation Failed. MaxLength Exceeded than specified for Attribute:", attribute["attributeName"])

                                # elif attribute["isRequired"] == "False":
                                #     maxLength = len(attribute["attributeMaxLength"])
                                #     check_length = self._SOURCE_DATA_DF.map \
                                #         (
                                #             lambda x : "True" if len(x.split("\t")[iColPos]) == 0 or len(x.split("\t")[iColPos]) <= maxLength else "False"
                                #         ).filter \
                                #         (
                                #             lambda x : x == "False"
                                #         )
                                #     if len(check_length.take(check_length.count())) != 0:
                                #         print("Wrong Data Found in check_length else condition")

                                # check for property isUnique
                            if attribute["isUnique"] == "True":
                                print(" Checking for Unique Data Type:")
                                totalCount = self._SOURCE_DATA_DF.count()
                                check_unique = self._SOURCE_DATA_DF.map \
                                    (
                                        lambda x : x.split("\t")[iColPos]
                                    )
                                check_unique = set(check_unique.take(check_unique.count()))
                                if totalCount != len(check_unique) :
                                    print("Error!!! Schema Validation Failed. Unique data expected for the attribute:", attribute["attributeName"])
                        print("Schema & Data validation turned off for the attribute:",attribute["attributeName"])
                        iColPos = iColPos + 1
                    return "True"
                else:
                    pass

        except Exception as e:
            print ("Error in validating Schema!!!", e)
            print(traceback.print_stack())
            return "False"

    def generateNewBatchId(self):
        try:
            batchId = uuid.uuid1()
        
            return batchId

        except Exception as e:
            print("Error!! Error in generating a unique Batch Id", e)

    def generateDCSystemDF(self,pDF):
        try:         
            #create a dataframe with just the RowId's initially and then append each of the constant values as a new column
            #dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"]) 
            dfSystem = pDF        
            dictSystemKeys = {}            
            
            for dcCols in self._DICT_ATTRIBUTES_DC_SYSTEM:  
                sAppendCol = dcCols["attributeName"]
                print("--> Attribute Name:", sAppendCol)
                if dcCols["attributeName"] == "siteCode":
                    dictSystemKeys[dcCols["attributeName"]] = self._SITE_CODE
                    dfSystem = dfSystem.withColumn(sAppendCol, lit(self._SITE_CODE))

                elif dcCols["attributeName"] == "organizationCode":
                    dictSystemKeys[dcCols["attributeName"]] = self._ORG_CODE 
                    dfSystem = dfSystem.withColumn(sAppendCol, lit(self._ORG_CODE))
                                            
                elif dcCols["attributeName"] == "entityCode":                                   
                    dictSystemKeys[dcCols["attributeName"]] = self._ENTITY_CODE 
                    dfSystem = dfSystem.withColumn( sAppendCol, lit(self._ENTITY_CODE))
                                            
                elif dcCols["attributeName"] == "moduleCode":                                  
                    dictSystemKeys[dcCols["attributeName"]] = self._MODULE_CODE  
                    dfSystem = dfSystem.withColumn( sAppendCol, lit(self._MODULE_CODE))

                elif dcCols["attributeName"] == "divCode":                                  
                    dictSystemKeys[dcCols["attributeName"]] = self._DIV_CODE  
                    dfSystem = dfSystem.withColumn( sAppendCol, lit(self._DIV_CODE))

                elif dcCols["attributeName"] == "objCode":                                  
                    dictSystemKeys[dcCols["attributeName"]] = self._OBJECT_CODE 
                    dfSystem = dfSystem.withColumn( sAppendCol, lit(self._OBJECT_CODE))

                # elif dcCols["attributeName"] == "batchId" and dcCols["attributeClass"] == "adbiz.standards.batchId":  
                #     batchId = str(generateNewBatchId())
                #     dfSystem = dfSystem.withColumn( sAppendCol, lit(batchId))

                else:                                    
                    dictSystemKeys[dcCols["attributeName"]] =  dcCols["attributeValue"] 
                    dfSystem = dfSystem.withColumn( sAppendCol, lit(dcCols["attributeValue"] ))
            
            return dfSystem

        except Exception as e:
            print(e)


    def generateDCConstantsDF(self, pDF):
        try:
            #dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"]) 
            dfConstants = pDF
            for dcCols in  self._DICT_ATTRIBUTES_DC_CONSTANT:        
                sAppendCol = dcCols["attributeName"]
                sAppendVal = dcCols["attributeValue"]
                print("--> Attribute Name:", sAppendCol)
                if  sAppendVal != "" or   sAppendVal is not None:
                    dfConstants = dfConstants.withColumn( sAppendCol, lit(sAppendVal))

            return dfConstants

        except Exception as e:
            print("Error!! Error in generating Derived columns based on Formula:", e)

    # TO DO 
    def generateDCFormulaDF(self, pDF):
        try:
            #dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"]) 
            dfFormula = pDF
            for dcCols in  self._DICT_ATTRIBUTES_DC_FORMULA:        
                sAppendCol = dcCols["attributeName"]
                print("--> Attribute Name:", sAppendCol)
                dfFormula = dfFormula.withColumn( sAppendCol, lit("Sample Data"))
            return dfFormula

        except Exception as e:
            print("Error!! Error in generating Derived columns based on Formula:", e)

    # TO DO 
    def generateDCFunctionDF(self, pDF):
        try:
            #dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"]) 
            dfFunction = pDF
            for dcCols in self._DICT_ATTRIBUTES_DC_FUNCTION:        
                sAppendCol = dcCols["attributeName"]
                print("--> Attribute Name:", sAppendCol)
                if dcCols["attributeDefaultValue"] != "":
                    dfFunction = dfFunction.withColumn( sAppendCol, lit(dcCols["attributeDefaultValue"]))
                else:
                    dfFunction = dfFunction.withColumn( sAppendCol, lit("Sample Data"))
            return dfFunction

        except Exception as e:
            print("Error!! Error in generating Derived columns based on functions:", e)

    # TO DO 
    def generateDCDateKeysDF(self, pDF):
        try:
            #dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"]) 

            dfDateKeys = pDF
            for dcCols in  self._DICT_ATTRIBUTES_DC_DATEKEYS:        
                print("--> Attribute Name:",dcCols["attributeName"]) 
                for k, v in self._PARTITION_DATEKEYS_DICT.items():
                    if k==dcCols["attributeName"]:
                        sDateKeys = v
                        sColName = "Id," +  sDateKeys
                        #sFormat =  dcCols["attributeFormat"] 
                        # for dtColName in sFormat:
                        #     sColName = sColName + "," + dtColName                             
                        iColPos = self._OBJECT_ATTRIBUTES.get(dcCols["attributeReference"])                                 
                        iColPos  = int(iColPos) - 1
                        if self._DATEPARTITION_TYPE == 'YQMD':        
                            print("--> Date Partition Type:", self._DATEPARTITION_TYPE )  
                            print("--> Partition Columns:",sColName) 
                                        
                            if dcCols["attributePattern"] == "DD-MM-YYYY":                                                                
                                #rddDateKeys = self._SOURCE_DATA_DF.map(lambda x: (x[0], x[1].split('\t')[iColPos][6:11] , '04', x[1].split("\t")[iColPos][3:5] , x[1].split("\t")[iColPos][0:2] ))                                    
                                myFunc =  udf (lambda x: datetime.strptime(x, '%d-%m-%Y'), DateType())
                                
                                myDF = self._SOURCE_DATA_DF.select ("Id", k)
                                #print(myDF.show())

                                dfTemp = myDF.select("Id", k , myFunc(col(k)).alias("TempDateTime"))    # convert string to date time                            
                                df = dfTemp.select("Id",  year("TempDateTime").alias(k + "_" +"year"), quarter("TempDateTime").alias(k + "_" + "quarter"), month("TempDateTime").alias(k + "_" + "month") , dayofmonth("TempDateTime").alias(k + "_" + "day"))                                
                                print("Merging Dataframes....")                                 
                                dfDateKeys = dfDateKeys.join(df,"Id", "outer" )  
                                #print(dfDateKeys.show())  
                                                                            
                                
                        return dfDateKeys        
                #currently implement for 1 Date Key Partition only #TODO                        
                        

        except Exception as e:
            print("Error!! Error in generating Derived columns based on Date Keys:", e)
            sys.exit()


    def saveData(self, pDF):
        try:
            # sc = SparkContext()
            # sqlContext = SQLContext(sc)
            # pDF = sqlContext.read.load("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\output.csv", format="csv" ,header = "true", interschema = "true")
            #df = sc.textFile("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\ST001\\ORG001\\ENT001\\ACTRBL\\input\\Invoices\\2018\\dfOutput.csv")

            
            print("***************************** Saving Datasets **********************************************")
            if self._DATASET["isIncrementalLoad"] == "True":
                for id, storages in self._DICT_TARGET_STORAGE.items(): 
                    print("Loading defined Target Storages from the data model.." )           
                    if storages["storageType"] ==  "PARQUET":
                        print("-> Storage Type:",storages["storageType"] )
                        for k, container in self._DICT_CONTAINERS.items():
                            sContainerCode = container["containerCode"]
                            sTarget = container["containerFolder"]                            
                            print("-> Location of Container:", sTarget) 
                            
                            if container["containerType"] == "Generic":                        
                                print(" -> Updating generic Container:",container["containerCode"] )
                                
                                sTarget = sTarget + "/" + sContainerCode
                                if container["isIncrementalLoad"] == "True":
                                    print("  -> Load Type: Incremental") 
                                    if container["isFirstTimeLoad"]  == "False":
                                        if storages["isPartitioned"] == "True":   
                                            sPartitions = self._PARTITION_KEYS 
                                            if sPartitions!="" or sPartitions is not None:
                                                print("  --> Using Partition Keys for the Container:", sPartitions)  
                                                pDF = pDF.withColumn("containerCode", lit(sContainerCode))                                                                                    
                                                #self.saveToParquet( pDF, sPartitions, sTarget, "append")
                                                print("  --> Container successfully Updated!!")
                                                print("  --> Creating/Saving Aggregates now..") 
                                                #self.saveAggregates(pDF, sContainerCode) 
                                            else:
                                                print(" --> No Partitions defined!!") 
                                    else:
                                        #todo: Create a new container with a UUID and add it to the partitions
                                        pass
                                else:
                                    #todo: For reloading the partitions (mode = Overwrite). Create a temp containers and then overwrite
                                    pass
                            elif container["containerType"] == "userSpecified":
                                    print("Updating user defined Container:",container["containerCode"])
                                    print(" --> Reading conditions for the user specified Container..", )
                                    lstConditions = container["conditions"]
                                    sConditions = self.readDFConditions(lstConditions) 
                                    sTarget = sTarget + "/" + sContainerCode
                                    if container["isIncrementalLoad"] == "True":
                                        print(" --> Load Type: Incremental") 
                                        if container["isFirstTimeLoad"]  == "False":
                                            if storages["isPartitioned"] == "True":                               
                                                sPartitions = self._PARTITION_KEYS 
                                                print(" --> Using Partition Keys:", sPartitions)                            
                                                if sConditions!="" or sConditions is not None:
                                                    #print(sConditions) 
                                                    sConditions = "invoiceStatus = 'Open'"
                                                    pDF = pDF.withColumn("containerCode", lit(sContainerCode))                                           
                                                    pDFCntr = pDF.filter(sConditions)
                                                    #self.saveToParquet( pDF, sPartitions, sTarget, "append")
                                                    print("  --> Container successfully Updated!! Updating Aggregates now..")
                                                    print("  --> Creating/Saving Aggregates now..")                                                
                                                    #self.saveAggregates(pDF, sContainerCode  )  
                                                    
                                            else:
                                                #todo: Create a new container with a UUID and add it to the partitions
                                                pass
                                    else:
                                        #todo: For reloading the partitions (mode = Overwrite). Create a temp containers and then overwrite
                                        pass
                                        #pDF.createOrReplaceTempView("dfTempCntnr")
                                        #print(" --> Saving Dataset into user defined Container.. ")

                                                    
                                                    
                                    #partitionBy(sPartitions.split(","))
                                    #pDF.write.partitionBy(sPartitions.split(",")).option("compression","snappy").parquet(sTarget, mode = 'append')
                    else:
                        # TODO  - Other Target Storage Types
                        pass
            elif self._DATASET["isIncrementalLoad"] == 'False':
                pass        
                
        except Exception as e:
            print("Error occurred during saving dataset:", e)
            print(traceback.print_stack())
            sys.exit()

    # Save Aggregates for single Container
    def saveAggregates(self, pDF, pContainerCode):
        try:            
            for k,v in self._DICT_AGGREGATES.items():
                sAggCode = v.get("aggCode")   
                sAggCategory = v.get("aggCategory")       
                if v.get("isActive") == "True":
                    lstContainers = v.get("containerCode")                                     
                    sContainerFolder = v.get("containerFolder")
                    if isinstance(lstContainers, list):
                        for container in lstContainers:
                            sContainerCode = str(container)                            
                            if sContainerCode == pContainerCode:                                
                                print("Performing Aggregations now on the Container:",sContainerCode)
                                print(" --> Aggregate Code:", sAggCode)
                                sTarget = v.get("aggFolder")
                                sTarget = sTarget + "/" + sAggCode   
                                print(" --> Target Location for Aggregates:", sTarget)
                                lstDim = v.get("dimensions")  
                                lstMeasures = v.get("measures")
                                dictMeasures = {}

                                for measure in lstMeasures:
                                    k = measure.get("attributeName")
                                    #print(" --> Measures:", measure.get("attributeName"))
                                    if measure.get("isActive") == 'True':
                                        dictMeasures[k] = measure

                                sAggKeys = self._COLUMNS_DC_SYSTEM
                                print(" --> System Aggregate Keys:", sAggKeys)
                                sAggKeys = sAggKeys + "," + "aggCode"
                                sAppendFlg = v.get("isAppend")
                                if sAppendFlg == "True":
                                    if v.get("isRebuild") == "False":
                                        print(" --> Appending Agggregates..")                                     
                                        myDF = pDF.withColumn("aggCode", lit(sAggCode)) # add the aggregate id as new column to the Dataframe
                                        #myDF = myDF.withColumn("containerId", lit(sContainerCode)) # add Container Id to the current Dataframe
                                if  sAppendFlg == "False":
                                    if v.get("isRebuild") == "True":
                                        print(" --> Rebuilding Agggregates..")
                                        #mySpark = self._SPARK_SESSION
                                        #dfCntnr = mySpark.read.load(sContainerFolder)        # Read the entire container                             
                                        #sSourceTable = self.getTargetHiveTable(self._SOURCE_DATA_MODEL,sContainerCode)
                                        #sSQL = "select * from " + sSourceTable
                                        #myDF = mySpark.sql(sSQL)
                                        #sTargetTable = self.getTargetHiveTable(self._SOURCE_DATA_MODEL,sAggCode)
                                        #myDF = dfCntnr.filter(col("aggCode")).isin(sAggCode)    # filter data for the current aggregate only

                                        if myDF is None:
                                            print("Warning!! No aggregate data found existing in the system. Rebuilding again.")
                                            myDF = pDF.withColumn("aggCode", lit(sAggCode)) 
                           
                                for dimension in lstDim:
                                    for k,v in dimension.items():
                                        if sAggCategory == 'TimeSeries':
                                            if k == "ByDate":    
                                                sAttribute = v.get("attributeName")     
                                                if sAttribute!="":                                 
                                                    print("  --> Agg Dimension (By Date):", v.get("dimCode"))
                                                    sDateKeys =  self._PARTITION_DATEKEYS_DICT[sAttribute]       # get the comma separated attributes part of the datekey dimension
                                                    sAggKeys=  sAggKeys + "," + sDateKeys
                                                
                                        if k == "ByLookup":
                                            sAttribute = v.get("attributeName") 
                                            if sAttribute!="":  
                                                print("  --> Agg Dimension (By Lookup):", v.get("dimCode"))
                                                sAggKeys = sAggKeys + "," + sAttribute
                                                print("  --> Aggregate Keys:", sAggKeys)
                                                    
                                        myAggDF = ""
                                        for k1,v1 in dictMeasures.items():
                                            lstMeasureType = v1["measureType"]
                                            lstOperators = v1["measureOperators"]
                                            print("  --> Measure:", k1)                                            
                                            myGrpDF = myDF.groupBy(sAggKeys.split(","))                                                
                                            for t in lstMeasureType:
                                                if t == "ByValue":
                                                    for o in lstOperators:
                                                        if o == "Sum":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg(sum(k1).alias("sum"))
                                                            #print(myAggDF.collect())
                                                        elif o == "Min":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'min'})
                                                            #print(myAggDF.collect())
                                                        elif o == "Max":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'max'})
                                                            #print(myAggDF.collect())
                                                        elif o == "Avg":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'avg'})
                                                            #print(myAggDF.collect())
                                                        elif o == "Mean":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'mean'})
                                                        elif o == "StdDev":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'stddev'})
                                                        elif o == "var":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'variance'})
                                                if t == "ByCount":
                                                    for o in lstOperators:
                                                        if o == "Count":
                                                            print("    --> Operator", o)
                                                            #myAggDF = myGrpDF.agg({k1:'count'})
                                                
                                            myDFTemp = myGrpDF.agg(sum(k1).alias(k1 + "_" + "SUM"), max(k1).alias(k1 + "_" + "MAX"), min(k1).alias(k1 + "_" + "MIN") , count(k1).alias(k1 + "_" + "COUNT"), avg(k1).alias(k1 + "_" + "AVG"), variance(k1).alias(k1 + "_" + "VAR"), stddev(k1).alias(k1 + "_" + "STDDEV"))
                                            #print(myDFTemp.show())
                                            if myAggDF == "" or myAggDF is None:
                                                myAggDF = myDFTemp
                                            else:
                                                myAggDF = myAggDF.join(myDFTemp,sAggKeys.split(","), "outer")
                                            
                                            print("  --> Completed Measure calculation:")
                                            #print(myAggDF.show())
                                        # For Loop Ends - Measures
                                    # for Loop ends  - Dimension list of values
                                # for Loop ends - Dimension list
                                        
                                #Save Aggregates for the single dimension and multiple measures
                                print(" --> Saving Aggregates now...")
                                if  sAppendFlg == "False":
                                    myAggDF.write.partitionBy(sAggKeys.split(",")).option("compression","snappy").parquet(sTarget, mode = 'overwrite')
                                    print(" --> Saving Aggregates to Parquet...")
                                    #self.saveToParquet( myAggDF, sAggKeys, sTarget, "overwrite")
                                elif sAppendFlg == "True":
                                    print(" --> Saving Aggregates to Parquet...")
                                    myAggDF.write.partitionBy(sAggKeys.split(",")).option("compression","snappy").parquet(sTarget, mode = 'append')
                                    #self.saveToParquet( myAggDF, sAggKeys, sTarget , "append")
                                    
                                            #sys.exit()
                    else:
                        pass # ToDo for rebuild aggregates

        except Exception as e:
            print("Error occurred during generating aggregates:", e)
            print(traceback.print_stack())
            sys.exit()

    def processKPIs(self, pAction):
        try:
            if self._DICT_KPIS is not None:
                for k,v in self._DICT_KPIS.items():
                    print("************************** Processing KPI **************************", k)
                    sCatalogType = v["catalogType"]
                    sKPICode = v["kpiCode"]
                    lstObjKPIData= []
                    sContainerCode = ""
                    sAggCode = ""
                    print(" --> Catalog Type:",sCatalogType)
                    if sCatalogType == "adbiz.catalogType.multiEntity.SOMOED":                       
                        dictCriterias = {}
                        dictMeasures = {}
                        lstSystemCols = []
                        sTargetPath = ""
                        sDateFilter = ""
                         

                        dictRoleFilters = v["roleFilter"]                    
                        print("  --> Adding Role  Filters")
                        lstEntities = dictRoleFilters["entityCode"]
                        lstSystemCols.append("entityCode")
                        if lstEntities[0] == "<ALL>":
                            pass        #TODO
                        
                        lstDivisions = dictRoleFilters["divCode"]
                        lstSystemCols.append("divCode")
                        if lstDivisions[0] == "<ALL>":
                            pass            #TODO
                        
                        dictStorageFilters = v["storageFilter"]
                        print("  --> Adding Storage Filters")
                        sContainerCode = dictStorageFilters["containerCode"]
                        sAggCode = dictStorageFilters["aggCode"]

                        dictSystemFilters = v["systemFilter"]
                        print("  --> Adding System Filters")
                        sSiteCode = dictSystemFilters["siteCode"]
                        lstSystemCols.append("siteCode")

                        sOrgCode  = dictSystemFilters["organizationCode"]
                        lstSystemCols.append("organizationCode")

                        sModCode = dictSystemFilters["moduleCode"]
                        lstSystemCols.append("moduleCode")

                        sObjCode = dictSystemFilters["objCode"]
                        lstSystemCols.append("objCode")

                        dictContainerDetails = self._DICT_CONTAINERS.get(sContainerCode)
                        dictAggDetails = self._DICT_AGGREGATES.get(sAggCode)
                        
                        sContainerPath = dictContainerDetails["containerFolder"]
                        sAggPath = dictAggDetails["aggFolder"]

                        if sAggPath is None:
                            print("Error!! No Aggregates exists at the given location:",sAggCode )
                            sys.exit()

                        sTargetPath = sContainerPath + "/"+ sContainerCode + "/" + "siteCode\=" + self._SITE_CODE + "/" + "organizationCode\=" + self._ORG_CODE + "/" + "moduleCode\=" + self._MODULE_CODE + "/" + "objCode\=" + self._OBJECT_CODE + "/"+  "containerCode\=" + sContainerCode                         
                        sTargetPath = sAggPath + "/" + sAggCode
                        print(" -> Aggregates Location (PARQUET):", sTargetPath)

                        #sTargetPath = "/home/setupadmin/adbiz/components/etl/output/actrbl/containers/CNT_ACTRBL_INVOICE_000/siteCode\=ST001/organizationCode\=ORG001/moduleCode\=ACTRBL/objCode\=invoice/containerId\=CNT_ACTRBL_INVOICE_000/"
                        #sTargetPath  = "/home/setupadmin/adbiz/components/etl/output/actrbl/containers/CNT_ACTRBL_INVOICE_000/siteCode\=ST001/organizationCode\=ORG001/moduleCode\=ACTRBL/objCode\=invoice/containerId\=CNT_ACTRBL_INVOICE_000/entityCode\=ORG001-ENT001/divCode\=DIV-A/invoiceDate_YEAR\=2019/invoiceDate_QUARTER\=3/invoiceDate_MONTH\=7/invoiceDate_DAY\=13"                      
                        print(" -> Loading KPI Components..")
                        for component in v["components"]:
                            print(" --> Processing Component:", component["componentCode"])
                            lstCriteriaColumns = []
                            lstGroupByColumns = []
                            lstSelectColumnsForKPI = []
                            lstDimValues = []
                           
                            sRecordType = component["recordType"]
                            sComponentType = component["componentType"] 
                            sComponentCode = component["componentCode"]
                            dictCriterias = component["criteria"]                        

                            sGroupBySQL = ""
                            sOrderBySQL = " ORDER BY "
                            
                            sSelectSQL = ""
                            dictMeasureOperators = {}
                            dictDateOperators = {}
                            sQuickOption = ""

                            for k,v in dictCriterias.items():
                                dictSortOrder = dictCriterias["sortBy"]  
                                iTopRows = int(dictCriterias["topRows"])
                                   
                                if k == "dimension":
                                    sDimCode = v["dimCode"]
                                    sDimAttribute = v["attributeName"]                                    
                                    if sDimAttribute != "":
                                        print("  --> Dimension:", sDimCode)
                                        lstCriteriaColumns.append(sDimAttribute)
                                        lstSelectColumnsForKPI.append(sDimAttribute)
                                        lstGroupByColumns.append(sDimAttribute)
                                        lstDimValues = v["dimSelectedValue"]
                                        

                                if k == "measure":
                                    for measure in v:
                                        dictMeasures[measure["measureCode"]] = measure  
                                        print("  --> Measure:", measure["measureCode"])
                                        #sSelectSQL = sSelectSQL + ","+  measure["attributeName"]
                                        lstMeasureConditions = measure["measureConditions"]
                                        for dictConditions in lstMeasureConditions:
                                            for k,v in dictConditions.items():
                                                if k == "operator":
                                                    sTempCol = measure["attributeName"] + "_" + v.upper()
                                                    print ("  --> Aggregate Cols:", sTempCol, "-", v)
                                                    lstCriteriaColumns.append(sTempCol)
                                                    dictMeasureOperators[v] = sTempCol

                                if k == "dateFilter":
                                    if v["datePartitionModel"] == "YQMD": 
                                        sDateAttribute = v["attributeName"]
                                        print("  --> Date Filter:", sDateAttribute )
                                        sQuickOption =  v["dateKey"]
                                        if v["quickOption"] == "previous":
                                            print("  --> Date Key:", v["dateKey"] )
                                            if v["dateKey"] == "month":
                                                iValue = int(v["value"])
                                                dtEnd = date.today()
                                                dtStart = dtEnd+relativedelta(months=-(iValue))
                                            elif v["dateKey"] == "day":
                                                iValue = int(v["value"])
                                                dtEnd = date.today()
                                                dtStart = dtEnd+relativedelta(days=-(iValue))
                                            elif v["dateKey"] == "year":
                                                iValue = int(v["value"])
                                                dtEnd = date.today()
                                                dtStart = dtEnd+relativedelta(years=-(iValue))
                                            elif v["dateKey"] == "quarter":
                                                iValue = int(v["value"])
                                                dtEnd = date.today()
                                                dtStart = dtEnd+relativedelta(months=-(iValue*3))   

                                        elif v["quickOption"] == "next":
                                            if v["dateKey"] == "month":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(months=+(iValue))
                                            elif v["dateKey"] == "day":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(days=+(iValue))
                                            elif v["dateKey"] == "year":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(years=+(iValue))
                                            elif v["dateKey"] == "quarter":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(months=+(iValue*3))
                                       
                                        elif v["quickOption"] == "current":
                                            if v["dateKey"] == "month":
                                                iValue = int(v["value"])
                                                dtStart = date.today() 
                                                dtEnd = dtStart+relativedelta(months=(iValue))
                                            elif v["dateKey"] == "day":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(days=(iValue))
                                            elif v["dateKey"] == "year":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(years=(iValue))
                                            elif v["dateKey"] == "quarter":
                                                iValue = int(v["value"])
                                                dtStart = date.today()
                                                dtEnd = dtStart+relativedelta(months=(iValue*3))
                                        
                                        elif v["quickOption"] == "between":
                                            dtStart = datetime.strptime(v["startDate"],"%d/%m/%Y")
                                            dtEnd = datetime.strptime(v["endDate"],"%d/%m/%Y")
                                            
                                        
                                        print('  --> Start Date:' , dtStart.strftime("%d/%m/%Y"))
                                        print('  --> End Date:' ,  dtEnd.strftime("%d/%m/%Y"))

                                        # Add Date Filters for the dataframe:
                                        
                                        sFilterAttributeYear = sDateAttribute + "_YEAR"
                                        iYear = int(dtStart.year)
                                        lstCriteriaColumns.append(sFilterAttributeYear)
                                        dictDateOperators['YEAR'] = sFilterAttributeYear
                                        

                                        sFilterAttributeMonth = sDateAttribute + "_MONTH"
                                        iMonth = int(dtStart.month)
                                        lstCriteriaColumns.append(sFilterAttributeMonth)
                                        dictDateOperators['MONTH'] = sFilterAttributeMonth

                                        sFilterAttributeQtr = sDateAttribute + "_QUARTER"
                                        #iQtr = int(dtStart.quarter)
                                        iQtr = 4
                                        lstCriteriaColumns.append(sFilterAttributeQtr)
                                        dictDateOperators['QUARTER'] = sFilterAttributeQtr

                                        sFilterAttributeDay = sDateAttribute + "_DAY"
                                        iDay = int(dtStart.day)
                                        lstCriteriaColumns.append(sFilterAttributeDay)
                                        dictDateOperators['DAY'] = sFilterAttributeDay

                            # Construct the final Dataframe filters and select columns for the current component
                            print(" -> Filtering KPI Data now..")
                            
                            sCols = ""
                            lstFinalCols = lstSystemCols + lstCriteriaColumns
                            for cols in lstFinalCols:
                                if sCols == "":
                                    sCols = cols
                                else:
                                    sCols = sCols + "," + cols   

                            print("  --> KPI Columns List:", sCols)                             
                            print("  --> Reading Aggregates now...")
                            myBaseDF = self._SPARK_SESSION.read.parquet(sTargetPath) \
                                        .filter(col("siteCode") == sSiteCode) \
                                        .filter(col("organizationCode") == sOrgCode) \
                                        .filter(col("moduleCode") == sModCode) \
                                        .filter(col("objCode") == sObjCode) \
                                        .filter(col("containerCode") == sContainerCode) \
                                        .filter(col("aggCode") == sAggCode) \
                                        .filter(col(sFilterAttributeYear) >= iYear) \
                                        .filter(col(sFilterAttributeMonth) >= iMonth)    \
                                        .filter(col(sFilterAttributeDay) >= iDay) 
                        
                            print("  --> Dimensions:", lstDimValues)
                            if len(lstDimValues) > 0:
                                myBaseDF = myBaseDF.filter(col(sDimAttribute).isin(lstDimValues)) 
                            
                            print("  --> Entities:", lstEntities[0], "  Divisions:", lstDivisions[0])
                            if lstEntities[0] == "<All>":
                                if lstDivisions[0] == "<All>":
                                    myDF = myBaseDF
                                else:
                                    myDF = myBaseDF.filter(col("divCode").isin(lstDivisions))
                            else:
                                if lstDivisions[0] == "<All>":
                                    myDF = myBaseDF.filter(col("entityCode").isin(lstEntities))                                      
                                else:
                                    myDF = myBaseDF.filter(col("divCode").isin(lstDivisions)).filter(col("entityCode").isin(lstEntities))     
                            
                            myDF = myDF.select(sCols.split(","))
                            iKPIRows = myDF.count() 
                            print("  --> KPI Rows:", iKPIRows)
                            if iKPIRows > 0:
                                sTableName = "st001_org001_actrbl" + "." + sComponentCode
                                #myDF.write.format('parquet').saveAsTable(sTableName)
                                dfNew = myDF.createOrReplaceTempView(sComponentCode)
                                                                
                                if len(lstDimValues) > 0:          
                                    sGroupBySQL = sDimAttribute
                                
                                
                                for k,v in dictMeasureOperators.items():  
                                    lstSelectColumnsForKPI.append(k + "(" + v + ") AS " + k.upper())                              
                                    # if sTemp == "":
                                    #     sTemp = k + "(" + v + ") AS " + k.upper()
                                    # else:
                                    #     sTemp = sTemp + "," + k + "(" + v + ") AS " + k.upper()
                                sKpiCol = ""
                                for cols in lstSelectColumnsForKPI:
                                    if sKpiCol == "":
                                        sKpiCol = cols
                                    else:
                                        sKpiCol = sKpiCol + "," + cols

                                sSelectSQL = "SELECT " +  sKpiCol 
                                                                
                                sTempOrder = ""
                                sSortOrder = dictSortOrder["sortOrder"]
                                sSortAttribute = dictSortOrder["attributeName"]
                                sSortOperator = dictSortOrder["operator"]
                                sSortCol = sSortAttribute + "_" + sSortOperator
                                if sQuickOption == 'year':
                                    sSelectSQL = sSelectSQL + "," + dictDateOperators.get("YEAR") + " AS PERIOD"
                                    if sGroupBySQL == "":
                                        sGroupBySQL =  dictDateOperators.get("YEAR")
                                    else:
                                        sGroupBySQL = sGroupBySQL + "," + dictDateOperators.get("YEAR")
                                if sQuickOption == 'quarter':
                                    sSelectSQL = sSelectSQL + ", concat(" + dictDateOperators.get("YEAR") + "," + "' Q('" + "," + dictDateOperators.get("QUARTER") + "," + "')') AS PERIOD"
                                    if sGroupBySQL == "":
                                        sGroupBySQL = dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER")
                                    else:
                                        sGroupBySQL = sGroupBySQL + "," + dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER")
                                if sQuickOption == 'month':
                                    sSelectSQL = sSelectSQL + ", concat(" + dictDateOperators.get("YEAR") + "," + "'-'" + "," + dictDateOperators.get("MONTH") + "," + "' Q('" + "," + dictDateOperators.get("QUARTER") + "," +  "')') AS PERIOD"
                                    if sGroupBySQL == "":
                                        sGroupBySQL = dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER") + "," + dictDateOperators.get("MONTH") 
                                    else:
                                        sGroupBySQL = sGroupBySQL + "," + dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER") + "," + dictDateOperators.get("MONTH") 
                                if sQuickOption == 'day':
                                    sSelectSQL = sSelectSQL + ", concat(" + dictDateOperators.get("DAY") + "," + "'-'" + ","+ dictDateOperators.get("MONTH") + "," + "'-'" + "," + dictDateOperators.get("YEAR") + "," + "' Q('" + "," + dictDateOperators.get("QUARTER") + "," + "')' ) AS PERIOD"
                                    if sGroupBySQL == "":
                                        sGroupBySQL = dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER") + "," + dictDateOperators.get("MONTH") + "," + dictDateOperators.get("DAY") 
                                    else:
                                        sGroupBySQL = sGroupBySQL + "," + dictDateOperators.get("YEAR") + "," + dictDateOperators.get("QUARTER") + "," + dictDateOperators.get("MONTH") + "," + dictDateOperators.get("DAY") 
        
                                sFinalSQL = sSelectSQL + " from " + sComponentCode + " GROUP BY " + sGroupBySQL
                                
                                print("  --> Final SQL:", sFinalSQL)
                                dfTemp = self._SPARK_SESSION.sql(sFinalSQL)                                

                                if sSortOperator != "":      # using measure operator as the sort by column                                
                                    if sSortOrder == "desc":
                                        dfSorted = dfTemp.orderBy(sSortOperator.upper(), ascending = False )
                                    elif sSortOrder == "asc":
                                        dfSorted = dfTemp.orderBy(sSortOperator.upper(), ascending = True )
                                else:
                                    if sSortOrder == "desc":
                                        dfSorted = dfTemp.orderBy(sSortCol, ascending = False )
                                    elif sSortOrder == "asc":
                                        dfSorted = dfTemp.orderBy(sSortCol, ascending = True )
                                
                                #print(dfSorted.show())

                                if iTopRows > 0 :
                                    dfFinal = dfSorted.limit(iTopRows)
                                else:
                                    dfFinal = dfSorted.limit(10)
                                
                                dictOutput={}
                                dictOutput[sComponentCode] = dfFinal.toJSON()
                                
                                print(dictOutput)
                                sTargetJson = "/home/setupadmin/adbiz/components/etl/output/" + sComponentCode + ".json"
                                dfFinal.coalesce(1).write.format('json').save(sTargetJson)
                                print("KPI Component Successfully saved!!!") 
                    else:
                        print("Error!! Incorrect Catalog Type specified:", sCatalogType)
                        sys.exit()
                            
        except Exception as e:
            print("Error!! Error in processing KPI's!!" , e )


    def saveToParquet(self, pDF, pPartitions, pTarget, pSaveMode):
        try:
            
            #sTargetObject = self.getTargetHiveTable(pCode)
            if pSaveMode == 'append':
                pDF.write.partitionBy(pPartitions.split(",")).option("compression","snappy").parquet(pTarget, mode = 'append')
            elif pSaveMode == 'overwrite':
                pDF.write.partitionBy(pPartitions.split(",")).option("compression","snappy").parquet(pTarget, mode = 'overwrite')
                
            #print("Target Table:", sTargetObject)
            #pDF.write.mode("append").format("parquet").saveAsTable(sTargetObject)  #.mode(pSaveMode) #option("mode",pSaveMode)
            print ("Data successfully saved!!:", pTarget)
        except Exception as e:
            print("Error!! Error in saving data to the target Repository!!!", e)
            sys.exit()
    
    def saveKPIData(self, pObjList):
        try:
            pass
        except Exception as e:
            print(e)

    def getTargetHiveTable(self, pCntnrId):
        try:
            #sTable = self._SOURCE_DATA_MODEL._HIVE_DB_NAME + "." + self._SOURCE_DATA_MODEL._HIVE_BASE_TABLE_NAME + "_" + pCntnrId
            sTable =  self._HIVE_BASE_TABLE_NAME + "_" + pCntnrId
            return sTable

        except Exception as e:
            print("Error!! Retrieving target Hive table details",e)


    def readDFConditions(self, pjsonData):
        try:
            dictSelectConditions = {}
            sSelectCol = ""
            sSelectCondition = ""
            sJoinCondition = ""
            for conditions in pjsonData: 
                sSelectCol = ""                                                                       
                for k,condition in conditions.items():                                  
                    sSelectCol =   conditions["attributeName"]                                                                                                                                                                     
                    if k == "subconditions":                                    
                        for subConditions in condition:  
                            
                            sSelectCondition = ""
                            sJoinCondition = ""
                            sVals = ""
                            sVal = "" 
                            sOperator = ""            

                            sOperator = subConditions["operator"]
                            sVals =  subConditions["value"]
                            if sOperator == " in ":                                            
                                for val in sVals:                                                
                                    if sVal !="":
                                        sVal = sVal + "," + val 
                                    else:
                                        sVal = val 
                                sSelectCondition  =  sOperator + str(sVal.split(","))  
                            elif sOperator == " == ":
                                sSelectCondition =  sOperator + sVals                                           
                                
                            sJoinCondition = subConditions["joinSubCondition"]
            
            return sSelectCondition                                                                    
                            

        except Exception as e:
            print(e)