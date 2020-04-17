import sys, getopt, traceback, os
import json
#import packages.utils.common as util
#from modules.actrbl.main import ClsAccountReceivables
from coreEngine.setup  import ClsEtlSettings, ClsEtlExecParameters
import coreEngine.commonUtils  as util
from coreEngine.commonModule import ClsCommonModule
argv = sys.argv[1:]
inputParameterFile =""  

sDisplayHelp = "Usage: main.py -i <inputParameterFile>"
try:
    
    opts, args  = getopt.getopt(argv, 'hi:',['help','ifile='])
    #print ("-->",opts, "-->", args)
    for opt, arg in opts:
        if opt == "-h":
            print (sDisplayHelp)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputParameterFile = arg
       
    if os.path.isfile(inputParameterFile):
        oETLParameters = ClsEtlExecParameters(inputParameterFile)          
        oEtlSettings = ClsEtlSettings()
        sSiteCode = oETLParameters._ETLEXEC_SITE_CODE
        sModuleCode = oETLParameters._ETLEXEC_MODULE_CODE       # check for valid modules TODO 
        sOrgCode = oETLParameters._ETLEXEC_ORG_CODE
        print("Executing ETL for Site:", sSiteCode)
        print(" -> Organization:", sOrgCode)
        print(' -> Module:', sModuleCode)        
            
        sQuery = {"siteCode":sSiteCode, "organizationCode":sOrgCode, "isActive":"True", "moduleCode":sModuleCode}
        sConditionType = ""
        sConditions = ""
        print("Reading Catalogs..")
        curCatalogs = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','catalogs', sQuery, sConditionType, sConditions)
        if curCatalogs is not None:                
            for catalog in curCatalogs:
                sCatalogName = catalog['catalogName']
                sCatalogCode = catalog['catalogCode']
                sCatalogType = catalog['catalogType']
                if sCatalogType == "adbiz.catalogType.multiEntity":         # System designed for particular hierarchy type
                    print("-> Catalog:", sCatalogCode)
                    print("Reading Data Models..")    
                    sQuery =    {"isActive":"True", "catalogCode":sCatalogCode} 
                    sConditionType=""
                    sConditions = ""
                    curDataModels =  util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datamodels', sQuery, sConditionType, sConditions)                    
                    if curDataModels is not None:                                               
                        for datamodel in curDataModels:                            
                            print("-> Reading Data Model:", datamodel['dataModelCode'])                           
                            sDataModelName = datamodel['dataModelName']   
                            sDataModelCode =   datamodel['dataModelCode']  
                            sObjectName = datamodel['objectName']
                            sQuery =    {"isActive":"True", "dataModelCode":sDataModelCode,"catalogCode":sCatalogCode} 
                            sConditions = "objectName"
                            sConditionType = "distinct"
                            
                            curObjects = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datamodels', sQuery, sConditionType, sConditions)
                            if curObjects is not None:
                                for object in curObjects:                                    
                                    sObjectName = object
                                    print("-> Reading Object:", sObjectName)  
                                    sQuery =    {"isActive":"True", "dataModelCode":sDataModelCode,"catalogCode":sCatalogCode, "objectName":sObjectName} 
                                    sConditions = ""
                                    sConditionType = ""
                                
                                    curDatasets = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datasets', sQuery, sConditionType, sConditions)
                                    if curDatasets is not None:                         
                                        for dataset in curDatasets:
                                            print("-> Reading Dataset:", dataset['datasetCode'])                                    
                                            sDatasetName = dataset['datasetName']
                                            sDatasetCode = dataset['datasetCode']
                                            lstDataSource = dataset['dataSource']
                                            if lstDataSource is not None:
                                                lstDataTarget = dataset['targetStorage']
                                                if lstDataTarget is not None:
                                                    sQuery =    {"isActive":"True", "catalogCode":sCatalogCode, "datasetCode":sDatasetCode} 
                                                    sConditions = "containerCode"
                                                    sConditionType = "distinct"
                                                    
                                                    lstContainers = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','containers', sQuery, sConditionType, sConditions)
                                                    
                                                    if lstContainers is not None:
                                                        print(" -> Containers to be processed:", lstContainers)

                                                        sQuery =    {"isActive":"True", "catalogCode":sCatalogCode, "datasetCode":sDatasetCode} 
                                                        sConditions = ""
                                                        sConditionType = ""
                                                        curContainers = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','containers', sQuery, sConditionType, sConditions)
                                                        dictContainers={}
                                                        for container  in curContainers:                                                            
                                                            dictContainers[container["containerId"]] = container                                                        
                                                        
                                                        sQuery =    {"isActive":"True", "catalogCode":sCatalogCode, "datasetCode":sDatasetCode} 
                                                        sConditions = "aggCode"
                                                        sConditionType = "distinct"
                                                        lstAggregates = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','aggregates', sQuery, sConditionType, sConditions)
                                                        if lstAggregates is not None:
                                                            print(" -> Aggregates to be processed:", lstAggregates)
                                                            sQuery =    {"isActive":"True", "catalogCode":sCatalogCode, "datasetCode":sDatasetCode} 
                                                            sConditions = ""
                                                            sConditionType = ""
                                                            curAggregates = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','aggregates', sQuery, sConditionType, sConditions)   
                                                            dictAggregates = {}
                                                            for aggregate in curAggregates:                                                            
                                                                dictAggregates[aggregate["aggId"]] = aggregate

                                                            
                                                            print(" -> KPI's to be processed")
                                                            dictKPIs={}
                                                            sQuery = {"siteCode":sSiteCode, "organizationCode":sOrgCode, "isActive":"True", "moduleCode":sModuleCode}
                                                            sConditions = ""
                                                            sConditionType = ""
                                                            curKPIs = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','kpis', sQuery, sConditionType, sConditions)
                                                            for kpi in curKPIs:
                                                                dictKPIs[kpi["kpiCode"]] = kpi
                                                                print(" -->", kpi["kpiCode"])

                                                            sQuery = {"isActive":"True", "calendarName": oETLParameters._ETLEXEC_CALENDAR} 
                                                            curCalendars =  util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','calendars', sQuery, sConditionType, sConditions)
                                                            if curCalendars is not None:
                                                                for calendar in curCalendars:
                                                                    #mySpark = oEtlSettings.startSparkContext() 
                                                                    mySpark=""
                                                                    print("Executing ETL for Module:", sModuleCode , "  and for object:", sObjectName)
                                                                    objModule = ClsCommonModule(mySpark, sModuleCode, oETLParameters, datamodel, sObjectName, dataset, dictContainers, dictAggregates, dictKPIs, calendar["dates"])
                                                                    #objModule.executeETL()
                                                                    objModule.processKPIs()
                                                                    # if sModuleCode == 'ACTRBL':
                                                                    #     sc = oEtlSettings.startSparkContext()                                                                                                                            
                                                                    #     #sc = ""
                                                                    #     oAccountRbl = ClsAccountReceivables(sc, oETLParameters, datamodel, sObjectName, dataset, dictContainers, dictAggregates, dictKPIs, calendar["dates"]) 
                                                                    #     oAccountRbl.executeETLForAccountReceivables(sc,oETLParameters, datamodel, sObjectName, dictContainers, dictAggregates, dictKPIs)
                                                                        
                                                                    #     #sc.stop()
                                                                    # elif sModuleCode == 'ACTPBL':
                                                                    #     pass
                                                            else:
                                                                print("Error!! No valid calendars found for the datamodel",sDataModelCode )
                                                                sys.exit()
                                                        else:
                                                            print("Error!! Aggregates are not defined for the datamodel:", sDataModelCode)
                                                    else:
                                                        print("Error!! Cotainers not defined for the Data model:", sDataModelCode)
                                                        sys.exit()
                                                else:
                                                    print("Error!!! No target storage defined for Object:", sObjectName)
                                            else:
                                                print("Error!!! No datasources defined for Object:", sObjectName)
                                                sys.exit()
                                    else:
                                        print("Error!! No datasets defined for the Object:", sObjectName)
                                        sys.exit(2)   
                            else:
                                print("Error!! Objects are not defined for ingestion in the data model:",sDataModelName)
                                sys.exit(2)  
                        else:
                            print("Error!! No valid data models defined for the catalog")
                            sys.exit(2)  
                    else:
                        print("Error!! Incorrect Catalog type specified.System cannot proceed!!")                                
                        sys.exit()                    
        else:
            print("Error!! No data catalogs defined for the specified Module:",sModuleCode , " for the Site:" ,sSiteCode  )   
            sys.exit(2)   

except getopt.GetoptError as e:
    print("Error in the input parameters!!!" ,e)    
    sys.exit(2)   
          
except Exception as e:
    print("Error!!!" ,e )
    print(traceback.print_stack())
    print (sDisplayHelp)

     
        


#if __name__== "__main__":
#    main(sys.argv[1:])
#    #main()