import sys, getopt, traceback, os
import json
import packages.utils.common as util
from modules.actpbl.main import ClsAccountPayables
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

        if oETLParameters._ETLEXEC_MODULE_CODE == "ACTPBL":           
            sQuery = {"siteCode":oETLParameters._ETLEXEC_SITE_CODE, "isActive":"True", "moduleCode":"ACTPBL"}
            sConditions = ""
            curCatalogs = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','catalogs', sQuery, sConditions)
            if curCatalogs is not None:
                for catalog in curCatalogs:                    
                    iCatalogId = catalog['catalogId']
                    sCatalogName = catalog['catalogName']
                    sCatalogCode = catalog['catalogCode']
                    sQuery =    {"isActive":"True", "catalogId":iCatalogId}  
                    curDatasets = util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datasets', sQuery, sConditions)
                    if curDatasets is not None:                         
                        for dataset in curDatasets:
                            iDatasetId = dataset['datasetId']
                            sDatasetName = dataset['datasetName']
                            sDatasetCode = dataset['datasetCode']
                            sObjectName = dataset['objectName']
                            sDataSource = dataset['dataSource']
                            sDataTarget = dataset['targetStorage']
                            sQuery =    {"isActive":"True", "datasetId":iDatasetId, "catalogId":iCatalogId} 
                            curDataModels =  util.executeDBQuery(oEtlSettings._METADATA_DB_CONN, 'site','datamodels', sQuery, sConditions)
                            if curDataModels is not None:
                                for datamodel in curDataModels:                                                                     
                                    curAttributes = datamodel['objectAttributes']  
                                    sDataModelName = datamodel['dataModelName']   
                                    sDataModelCode =   datamodel['dataModelCode']                              
                                    if sObjectName=='invoice':                              
                                        oAccountPbl = ClsAccountPayables('invoice',curAttributes)                                         
                                        oAccountPbl._ORG_CODE = oETLParameters._ETLEXEC_ORG_CODE
                                        oAccountPbl._SITE_CODE = oETLParameters._ETLEXEC_SITE_CODE
                                        oAccountPbl._CATALOG_NAME = sCatalogName
                                        oAccountPbl._DATAMODEL_NAME = sDataModelName
                                        oAccountPbl._DATASET_NAME =  sDatasetName  
                                        oAccountPbl._DATAMODEL_CODE = sDataModelCode
                                        oAccountPbl._DATASET_CODE =  sDatasetCode    
                                        oAccountPbl._CATALOG_CODE = sCatalogCode 
                                        oAccountPbl._DATA_SOURCE = (sDataSource)
                                        oAccountPbl._DATA_TARGET = sDataTarget  
                                        oAccountPbl.loadSourceData()                                           
                                        oAccountPbl.validateSchema(sObjectName)
                            else:
                                print("Error!! No valid data models defined for the catalog")
                                sys.exit(2)
                               
                    else:
                        print("Error!! No datasets defined for the Catalog")
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