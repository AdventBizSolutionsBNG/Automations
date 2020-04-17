import os
import yaml
import sys


class ClsDbConfig():

    _DB_SERVER_NAME = ""
    _DB_USER_NAME = ""
    _DB_PASSWORD = ""
    _DB_DATABASE_NAME = "" 
    _DB_PORT = ""
    _DB_CONFIG_FILE = ""

    def _init_(self):
        try:            
            baseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dbFile = str(os.path.join(os.path.sep, baseDir, 'adbizWebAPI','config', 'db.yaml'))
            print("Reading DB Config File:",dbFile)
            self._DB_CONFIG_FILE = dbFile            
            if os.path.exists(dbFile):
                print("Reading DB Config File:",dbFile)
                self.readDB(dbFile)
            else:
                print("Error!! Database config file not found..", dbFile)
                 
        except Exception as e:
            print (e)
            sys.exit()
            
    def readDB(self, pConfigFile):
        try:
            with open(pConfigFile,"r") as f:
                    config_items = yaml.full_load(f)
                    for items, v in config_items.items():                        
                        if items=='mysql':                            
                            self._DB_SERVER_NAME = v["server"]                           
                            self._DB_USER_NAME = v["user"]
                            self._DB_PASSWORD = v["password"]
                            self._DB_PORT = v["port"] 
                            self._DB_DATABASE_NAME = v["database"]

                    print("DB Settings initialized....")                  
                     
        except Exception as e:
            print(e)