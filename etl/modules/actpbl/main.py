from pymongo import MongoClient
import os,sys,traceback
import json
from etl import ClsEtlSettings
import packages.utils.common 
from packages.utils.common import jsonExtractElement
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext 
import pandas as pd

class ClsAccountPayables():
    _ACTPBL_INVOICE_CATALOG = {}    
    _SITE_CODE = ""
    _ORG_CODE = ""
    _CATALOG_CODE = ""
    _DATASET_CODE = ""
    _DATAMODEL_CODE = ""
    _CATALOG_NAME = ""
    _DATASET_NAME = ""
    _DATAMODEL_NAME = ""    
    _DATA_SOURCE = {}
    _DATA_TARGET = {}
    _FLG_VALIDATE = ""
    _RDD_SOURCE =""



    def __init__(self,pObjectType,pDoc):         
        if pObjectType=="invoice":
            for k in pDoc:             
                self._ACTPBL_INVOICE_CATALOG[k['attributeName']] = k
                print("--->" , k['attributeName'])
            
     
    def loadSourceData(self):
        try:
            print('Loading Account Payables Datasets') 
            print("Reading Source Data...")
            for sourceConfig in self._DATA_SOURCE:
                if sourceConfig['dataSourceType'] == "FILE":                   
                    if sourceConfig['folderPathPattern'] == "" or sourceConfig['folderPathPattern'] is None:                        
                        if sourceConfig['fileNamePattern'] =="" or   sourceConfig['fileNamePattern']  is None:                          
                            sSourceFile = sourceConfig['folderPath'] + "\\" + sourceConfig['fileName']  + "." +  sourceConfig['fileExtn']  
                            
                            if os.path.isfile(sSourceFile):
                                if(sourceConfig['isZipped']) == 'False':
                                    if(sourceConfig['isPassword']) == 'False' or (sourceConfig['isPassword']) == "":                                        
                                        sSeparator = sourceConfig['separator']
                                        if sSeparator == "\t":
                                            print("->", sourceConfig['startRow'])
                                            iSkipRows = int(sourceConfig['startRow'])
                                            iEndRows = int(sourceConfig['endRow'])
                                            sc = SparkContext("local","readSource")
                                            sample = sc.textFile(sSourceFile)
                                            sample_start = sc.parallelize(sample.take(iSkipRows))
                                            sample_sub = sample.subtract(sample_start)
                                            sample_end = sample.subtract(sc.parallelize(sample.take(sample.count() + iEndRows)))
                                            self._RDD_SOURCE = sample_sub.subtract(sample_end)

                                            #
                                            #rddSource = sc.textFile(sSourceFile).filter(lambda x: x[1] > sSkipLines).map(lambda line: line.split("\t"))
                                            #sample = sc.textFile(sSourceFile)
                                            #self._RDD_SOURCE = sc.parallelize(sample.take(int(sourceConfig['startRow'])))
                                            # sample_sub = sample.subtract(sample_start)
                                            # sample_end = sample.subtract(sc.parallelize(sample.take(sample.count() + int((sourceConfig['endRow'])))))
                                            # self._RDD_SOURCE = sample_sub.subtract(sample_end)
                                            
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
            print("Error in loading Data Catalog for Account Payables module!!", e)
            print(traceback.print_stack())


    def validateSchema(self, pObjectType):
        try:
            if pObjectType == "invoice":
                attributes = []
                seq = 0
                for key,value in self._ACTPBL_INVOICE_CATALOG.items():                     
                    attributes.append((key,seq))
                    seq += 1
                
                for attribute in attributes:
                    print(attribute[0])
                    print(self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isIgnore") )
                    if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isIgnore") == "False":
                        if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isValidateData") == "True":
                            # check for property String
                            if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("attributeDataType") == "string":
                                if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "True":
                                    check_string = self._RDD_SOURCE.map \
                                        (
                                            lambda x : "True" if str(type(x.split("\t")[attribute[1]])) == "<type 'unicode'>" and len(x.split("\t")[attribute[1]]) > 0 else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_string.take(check_string.count())) != 0:
                                        print("Wrong Data Found in check_string if condition:")
                                elif self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "False":
                                    check_string = self._RDD_SOURCE.map \
                                        (
                                            lambda x: "True" if len(x.split("\t")[attribute[1]]) == 0 or str(type(x.split("\t")[attribute[1]])) == "<type 'unicode'>" else "False"
                                        ).filter \
                                        (
                                            lambda x: x == "False"
                                        )
                                    if len(check_string.take(check_string.count())) != 0:
                                        print("Wrong Data Found in check_string else condition")

                            # check for property integer
                            if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("attributeDataType") == "integer":
                                if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "True":
                                    numbers = set([str(num) for num in range(0,10)])
                                    check_integer = self._RDD_SOURCE.map \
                                        (
                                            lambda x : "True" if len(set([num for num in x.split("\t")[attribute[1]]]).difference(numbers)) == 0 and len(x.split("\t")[attribute[1]]) > 0 else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_integer.take(check_integer.count())) != 0:
                                        print("Wrong Data Found in check_integer if condition")
                                elif self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "False":
                                    numbers = set([str(num) for num in range(0, 10)])
                                    check_integer = self._RDD_SOURCE.map \
                                        (
                                            lambda x: "True" if len(set([num for num in x.split("\t")[attribute[1]]]).difference(numbers)) == 0 and len(x.split("\t")[attribute[1]]) > 0 else "False"
                                        ).filter \
                                        (
                                            lambda x: x == "False"
                                        )
                                    if len(check_integer.take(check_integer.count())) != 0:
                                        print("Wrong Data Found in check_integer else condition")
                                        
                            # check for property attributeMaxLength
                            if int(self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("attributeMaxLength")) > 0:
                                if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "True":
                                    maxLength = int(self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("attributeMaxLength"))
                                    check_length = self._RDD_SOURCE.map \
                                        (
                                            lambda x : "True" if len(x.split("\t")[attribute[1]]) == 0 and len(x.split("\t")[attribute[1]]) <= maxLength else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_length.take(check_length.count())) != 0:
                                        print("Wrong Data Found in check_length in if condition")
                                elif self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isRequired") == "False":
                                    maxLength = len(self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("attributeMaxLength"))
                                    check_length = self._RDD_SOURCE.map \
                                        (
                                            lambda x : "True" if len(x.split("\t")[attribute[1]]) == 0 or len(x.split("\t")[attribute[1]]) <= maxLength else "False"
                                        ).filter \
                                        (
                                            lambda x : x == "False"
                                        )
                                    if len(check_length.take(check_length.count())) != 0:
                                        print("Wrong Data Found in check_length else condition")

                            # check for property isUnique
                            if self._ACTPBL_INVOICE_CATALOG.get(attribute[0]).get("isUnique") == "True":
                                totalCount = self._RDD_SOURCE.count()
                                check_unique = self._RDD_SOURCE.map \
                                    (
                                        lambda x : x.split("\t")[attribute[1]]
                                    )
                                check_unique = set(check_unique.take(check_unique.count()))
                                if totalCount != len(check_unique) :
                                    print("Wrong Data Found in check_unique if condition")
               
        except Exception as e:
            print ("Error in validating Schema!!!", e)
            print(traceback.print_stack())