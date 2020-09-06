import os
import yaml
import sys
import json
import logging

log = logging.getLogger("main")

class ClsDbConfig:
    _DB_SERVER_NAME = ""
    _DB_USER_NAME = ""
    _DB_PASSWORD = ""
    _DB_DATABASE_NAME = ""
    _DB_PORT = ""
    _DB_CONFIG_FILE = ""
    _DB_ENGINE = ""

    def __init__(self, db_file, module):
        try:
            print("Initializing DB Configuration!!")
            if os.path.exists(db_file):
                print("Reading DB Config File:", db_file)
                if self.read_config(db_file, module):
                    print("Successfully read DB config of Core Engine!!")
                else:
                    sys.exit()
            else:
                print("Error!! Database config file not found..")
                sys.exit()

        except Exception as e:
            print("Error occurred in initializing DB config of Core Engine!!", exc_info=True)
            sys.exit()

    def read_config(self, configfile, module):
        try:
            with open(configfile, "r") as f:
                config_items = json.load(f)

            for k, v in config_items.items():
                for items in v:
                    if items["module"] == module:
                        credentials = items["credentials"]
                        self._DB_SERVER_NAME = credentials["server"]
                        self._DB_DATABASE_NAME = credentials["database"]
                        self._DB_USER_NAME = credentials["user"]
                        self._DB_PASSWORD = credentials["password"]
                        self._DB_PORT = credentials["port"]
                        self._DB_ENGINE = credentials["engine"]

            print("DB Settings initialized for module:", module)
            return True
        except Exception as e:
            print("Error occurred in reading DB config of Core Engine!!", exc_info=True)
            return False

    def server(self):
        return self._DB_SERVER_NAME

    def user(self):
        return self._DB_USER_NAME

    def password(self):
        return self._DB_PASSWORD

    def port(self):
        return self._DB_PORT

    def dbname(self):
        return self._DB_DATABASE_NAME

    def engine(self):
        return self._DB_ENGINE
