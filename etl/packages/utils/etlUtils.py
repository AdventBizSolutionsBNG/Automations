import os,sys,traceback
import json
from datetime import datetime
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

from pyspark.sql.functions import lit, when, col, regexp_extract 

def importData(pSparkContext, pDataSources):
    try:           
        for dataSource in pDataSources:
            if dataSource['storageType'] == "FILE":                   
                if dataSource['folderPathPattern'] == "" or dataSource['folderPathPattern'] is None:                        
                    if dataSource['fileNamePattern'] =="" or   dataSource['fileNamePattern']  is None:                          
                        sSourceFile = dataSource['folderPath'] + "\\" + dataSource['fileName']  + "." +  dataSource['fileExtn']                              
                        if os.path.isfile(sSourceFile):
                            if(dataSource['isZipped']) == 'False':
                                if(dataSource['isPassword']) == 'False' or (dataSource['isPassword']) == "":                                        
                                    sSeparator = dataSource['separator']
                                    if (sSeparator == "\t" or sSeparator == ","):  
                                        print("Reading Source File:", sSourceFile)                                           
                                        iSkipRows = int(dataSource['startRow'])
                                        iEndRows = int(dataSource['endRow'])
                                        #sc = SparkContext("local","readSource")
                                        if iSkipRows >= 0:
                                            if iEndRows >= 0:
                                                rddSourceData = pSparkContext.textFile(sSourceFile).zipWithIndex().filter(lambda x: x[1] >=iSkipRows).filter(lambda y: y[1] <= iEndRows)
                                            elif iEndRows <0:
                                               pass                                               
                                        else:
                                            pass

                                        #sample_start = pSparkContext.parallelize(sample.take(iSkipRows))
                                        #sample_sub = sample.subtract(sample_start)
                                        #sample_end = sample.subtract(pSparkContext.parallelize(sample.take(sample.count() + iEndRows)))
                                        #rddSourceData = sample_sub.subtract(sample_end)
                                        return (rddSourceData)
                                        #
                                        #rddSource = sc.textFile(sSourceFile).filter(lambda x: x[1] > sSkipLines).map(lambda line: line.split("\t"))
                                        #sample = sc.textFile(sSourceFile)
                                        #pRddSource = sc.parallelize(sample.take(int(dataSource['startRow'])))
                                        # sample_sub = sample.subtract(sample_start)
                                        # sample_end = sample.subtract(sc.parallelize(sample.take(sample.count() + int((dataSource['endRow'])))))
                                        # pRddSource = sample_sub.subtract(sample_end)
                                        
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


def validateSchema(pSparkContext, pDictDataModel, pRddSource):
    try:
        # attributes = []
        # seq = 0
        # for key in pDictDataModel.items():   
        #     #print("-->",key)                  
        #     attributes.append((key,seq))
        #     seq += 1
        return "True"
        for  key, attributes in pDictDataModel.items():
            if(key =="objectAttributes"):    
                iColPos = 0                
                for attribute in attributes:                        
                    if attribute["isValidateData"]=="True":
                        print("--> Validating Schema for attribute:",attribute["attributeName"], " --> Attribute Data Type:", attribute["attributeDataType"] , "--> ColPosition:", (iColPos))
                        if attribute["attributeDataType"] == "string":
                            if attribute["isRequired"]=="True":
                                check_string = pRddSource.map \
                                    (
                                        lambda x : "True" if str(type(x.split("\t")[iColPos])) == "<type 'unicode'>" and len(x.split("\t")[iColPos]) > 0 else "False"
                                    ).filter \
                                    (
                                        lambda x : x == "False"
                                    )
                                if len(check_string.take(check_string.count())) != 0:
                                    print("Error!!! Schema Validation Failed.DataType String expected for Attribute:", attribute["attributeName"])
                            # elif attribute["isRequired"]=="False":
                            #     check_string = pRddSource.map \
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
                                check_integer = pRddSource.map \
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
                            #     check_integer = pRddSource.map \
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
                                check_length = pRddSource.map \
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
                            #     check_length = pRddSource.map \
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
                            totalCount = pRddSource.count()
                            check_unique = pRddSource.map \
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

def generateDerivedColumns(oAR, pSparkContext, pDictDataModel, pETLParams, pRddSource, pCalendar):
    try:
        #load a dictionary with the Id & Attributes Details
        
        dictAttributes = {}
        dfDateKeys=""
        dfConstants = ""
        dfSource = ""
        sSourceColNames = ""
        
        for k in oAR._DATA_SOURCE:
            sArchiveLoc = k["archiveFolderPath"]
            sErrorLoc = k["errorFolderPath"]
            isArchive = k["isArchive"]
            sFileName= k["fileName"]
            sTargetFileName = sArchiveLoc + "\\" + sFileName + "-" +  str(datetime.now().strftime("%Y%m%d-%H-%M-%S")) + ".csv"
            print(sTargetFileName)
              
    
        dfKeys = pRddSource.map(lambda x: (x[1],)).toDF(["Id"])         

        for  key, attributes in pDictDataModel.items():
            if(key =="objectAttributes"):
                print("Loading Attributes....")
                for attribute in attributes: 
                    if sSourceColNames == "":
                        sSourceColNames =  attribute["attributeName"]                  
                    else:
                        sSourceColNames =  sSourceColNames + "," + attribute["attributeName"]
                    dictAttributes[attribute["attributeName"]] = attribute["_id"]
        #print("Schema Structure:", sSourceColNames)
        sSourceColNames = "Id,RawData"
        dfSource = pRddSource.map(lambda x: (x[1], x[0].split("\t"))).toDF(sSourceColNames.split(","))
        #print(dfSource.show())       

        for  key, attributes in pDictDataModel.items():
            if(key =="derivedColumns"):                              
                dfConstants = dfKeys
                for derivedColumns in attributes:    
                    for derivedByKey, derivedByVal in derivedColumns.items():  
                        print("-->Derived Columns Category:", derivedByKey)                                             
                        if (derivedByKey == "derivedByConstants"): 
                            dictConstantKeys = {}                          
                            for seq in derivedByVal:
                                sAppendCol = seq["attributeName"]
                                print("Attribute Name:", sAppendCol)
                                if seq["attributeName"] == "siteCode":
                                    dictConstantKeys[seq["attributeName"]] = pETLParams._ETLEXEC_SITE_CODE
                                    dfConstants = dfConstants.withColumn( sAppendCol, lit(pETLParams._ETLEXEC_SITE_CODE))

                                elif seq["attributeName"] == "organizationCode":
                                    dictConstantKeys[seq["attributeName"]] = pETLParams._ETLEXEC_ORG_CODE 
                                    dfConstants = dfConstants.withColumn( sAppendCol, lit(pETLParams._ETLEXEC_ORG_CODE))
                                                            
                                elif seq["attributeName"] == "entityCode":                                   
                                    dictConstantKeys[seq["attributeName"]] = pETLParams._ETLEXEC_ENTITY_CODE 
                                    dfConstants = dfConstants.withColumn( sAppendCol, lit(pETLParams._ETLEXEC_ENTITY_CODE))
                                                           
                                elif seq["attributeName"] == "moduleCode":                                  
                                    dictConstantKeys[seq["attributeName"]] = pETLParams._ETLEXEC_MODULE_CODE  
                                    dfConstants = dfConstants.withColumn( sAppendCol, lit(pETLParams._ETLEXEC_MODULE_CODE))
                                else:                                    
                                    dictConstantKeys[seq["attributeName"]] =  seq["attributeValue"] 
                                    dfConstants = dfConstants.withColumn( sAppendCol, lit(seq["attributeValue"] ))
                                    
                        # TO DO
                        if derivedByKey == "derivedByFormula":
                            for seq in derivedByVal:
                                print(seq["attributeName"])

                        #TO DO
                        if derivedByKey == "derivedByFunction":
                            for seq in derivedByVal:
                                print(seq["attributeName"])                       
                        
                                                                    
                        if (derivedByKey == "derivedByDateKeys"):
                            dfDateKeys = dfKeys 
                            for seq in derivedByVal: 
                                print("Attribute Name:",seq["attributeName"])
                                sColName = "Id,"    
                                sColName = sColName + seq["attributeName"]                                
                                iColPos = dictAttributes.get(seq["attributeReference"])                                 
                                iColPos  = int(iColPos) - 1
                                if seq["attributePattern"] == "DD-MM-YYYY":                                                                
                                    rddDateKeys = pRddSource.map(lambda x: (x[1], x[0].split('\t')[iColPos][6:11] + x[0].split("\t")[iColPos][3:5] + x[0].split("\t")[iColPos][0:2]))                                    
                                    df = rddDateKeys.toDF(sColName.split(",")) 
                                    #print(df.show())  
                                    print("Merging Dataframes....")                                 
                                    dfDateKeys = dfDateKeys.join(df,"Id", "outer" )                                    
                                    #print(dfDateKeys.show())                                
                    
                                     
        #Merging Dataframes for Constants & Derived Columns        
        if dfDateKeys!="" and dfConstants!="":
            #print(dfConstants.show())
            #print(dfDateKeys.show())   
            print("Generating final Dataset...")
            dfNew = dfConstants.join(dfDateKeys,"Id", "outer")                  
            print(dfNew.show())
            dfFinal = dfNew.join(dfSource, dfNew.Id == dfSource.Id,"inner" )
            print(dfFinal.show())
            return dfFinal
            #dfFinal.write.csv(sTargetFileName)
                
    except Exception as e:
        print("Error!! Generating Derived Columns:",e)
        print(traceback.print_stack())
        sys.exit()

def saveData( pBO, pDF, pTargets):
    try:
        # sc = SparkContext()
        # sqlContext = SQLContext(sc)
        # df = sqlContext.read.load("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\ST001\\ORG001\\ENT001\\ACTRBL\\input\\Invoices\\2018\\dfOutput.csv", format="csv" ,header = "true", interschema = "true")
        # print(df.count())
        
        #df = sc.textFile("C:\\Mywork\\Advent\\ETLFramework\\etl\\data\\ST001\\ORG001\\ENT001\\ACTRBL\\input\\Invoices\\2018\\dfOutput.csv")
        print('Saving Data for the datasets')        
        for id, storages in pTargets.items():            
            if storages["storageType"] == "PARQUET":
                print("-> Storage Target:",storages["storageType"]  )
                sTarget = storages["targetFolder"]
                print("-> Target Location:", sTarget)
                if storages["isPartitioned"] == "True":
                    for k,v in pBO._PARTITION_KEYS.items():
                        sPartitions = v                        
                        #partitionBy(sPartitions.split(","))
                        pDF.write.partitionBy(sPartitions.split(",")).option("compression","snappy").parquet(sTarget, mode = 'append')
                        sys.exit()
            
            #for storage in storages:
                
            
    except Exception as e:
        print("Error occurred during saving data:", e)
        print(traceback.print_stack())
        sys.exit()


def createAggregates(pBO, pDF, pTargets):
    try:
        pass

    except Exception as e:
        print("Error occurred during generating aggregates:", e)
        print(traceback.print_stack())
        sys.exit()
