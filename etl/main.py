import sys, getopt, traceback, os
import json
import packages.utils.common as util
from modules.actrbl.main import ClsAccountReceivables
from etl import ClsEtlSettings, ClsEtlExecParameters

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
        print("Executing ETL for Site:", oETLParameters._ETLEXEC_SITE_CODE)
        print('-> Module:',oETLParameters._ETLEXEC_MODULE_CODE)
        if oETLParameters._ETLEXEC_MODULE_CODE == "ACTRBL":           
            sQuery = {"siteCode":oETLParameters._ETLEXEC_SITE_CODE, "isActive":"True", "moduleCode":oETLParameters._ETLEXEC_MODULE_CODE}
            sConditionType = ""
            sConditions = ""
            curCatalogs = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','catalogs', sQuery, sConditionType, sConditions)
            if curCatalogs is not None:                
                for catalog in curCatalogs:                               
                    sCatalogName = catalog['catalogName']
                    sCatalogCode = catalog['catalogCode']
                    print("-> Reading Catalog:", sCatalogCode)
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
                            curObjects = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datasets', sQuery, sConditionType, sConditions)
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
                                                        dictContainer={}
                                                        for container  in curContainers:                                                            
                                                            dictContainer[container["containerId"]] = container
                                                        
                                                        sQuery = {"isActive":"True", "calendarName": oETLParameters._ETLEXEC_CALENDAR} 
                                                        curCalendars =  util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','calendars', sQuery, sConditionType, sConditions)
                                                        if curCalendars is not None:
                                                            for calendar in curCalendars:
                                                                if oETLParameters._ETLEXEC_MODULE_CODE == 'ACTRBL':
                                                                    #sc = oEtlSettings.startSparkContext()                                                    
                                                                    sc=""
                                                                    
                                                                    #oAccountRbl = ClsAccountReceivables(sc, datamodel,oETLParameters,dataset,calendar) 
                                                                    #oAccountRbl.executeETLForAccountReceivables(sc, datamodel,oETLParameters,calendar["dates"])
                                                                    #sc.stop()
                                                                elif oETLParameters._ETLEXEC_MODULE_CODE == 'ACTPBL':
                                                                    pass
                                                        else:
                                                            print("Error!! No valid containers found for the dataset",sDatasetCode )
                                                            sys.exit()
                                                    else:
                                                        print("Error!! Calendar not defined for this ETL:", oETLParameters._ETLEXEC_CALENDAR)
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
            print("Error!! No data catalogs defined for the specified Module:",oETLParameters._ETLEXEC_MODULE_CODE , " for the Site:" ,oETLParameters._ETLEXEC_SITE_CODE  )   
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