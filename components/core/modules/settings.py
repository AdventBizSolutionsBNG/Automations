import json
import os
import sys
import logging
from logging.config import dictConfig
#from packages.logger import Logger
from components.core.packages.logger import Logger
from components.core.modules.storageEngines import DataLakeStorage
from components.core.modules.calendarEngine import CalendarEngine

log = logging.getLogger("main")

class Settings:
    _constants = {}
    _messages = {}
    _master = {}
    _lookups = {}
    _display_components = {}
    _charts = {}

    _constants_file_location = ""
    _messages_file_location = ""
    _master_file_location = ""
    _lookups_file_location = ""
    _calendar_datasets = ""
    _datalake_storage = ""

    def __init__(self, sfile):
        try:
            # initialize logging object
            with open(sfile, "r") as l:
                ldata = json.load(l)

                print("Initializing Logging system..")
                for k, v in ldata.items():
                    if k == "logging":
                        for k1, config in v.items():
                            if k1 == "logging_config":
                                Logger(config)
                                log=logging.getLogger("main")

            log.info("Initializing Core Engine Parameters..")
            with open(sfile, "r") as f:
                fdata = json.load(f)

            for k, v in fdata.items():
                if k == "data_lake_storage":
                    self._datalake_storage = DataLakeStorage(v)

                if k == "calendars":
                    self._calendar_datasets = CalendarEngine(v).get_calendar_data()

                if k == "metaData":
                    for config in v:
                        for k1, v1 in config.items():
                            if k1 == "display_components":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Constants..")
                                                self._constants_file_location = v1["file"]["location"]
                                                self.load_display_components()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.error("Settings provided in an incorrect data format. Cannot proceed!!")

                            if k1 == "charts":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Charts..")
                                                self._constants_file_location = v1["file"]["location"]
                                                self.load_charts()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.error("Settings provided in an incorrect data format. Cannot proceed!!")

                            if k1 == "constants":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Constants..")
                                                self._constants_file_location = v1["file"]["location"]
                                                self.load_constants()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.error("Settings provided in an incorrect data format. Cannot proceed!!")
                            elif k1 == "messages":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Messages..")
                                                self._messages_file_location = v1["file"]["location"]
                                                self.load_messages()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.info("Settings provided in an incorrect data format. Cannot proceed!!")
                            elif k1 == "master":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Masters..")
                                                self._master_file_location = v1["file"]["location"]
                                                self.load_master()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.error("Settings provided in an incorrect data format. Cannot proceed!!")
                            elif k1 == "lookups":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading lookups..")
                                                self._lookups_file_location = v1["file"]["location"]
                                                self.load_lookups()
                                            else:
                                                log.error("Settings files is zipped. Cannot proceed!!")
                                        else:
                                            log.error("Settings file is password protected. Cannot proceed!!")
                                    else:
                                        log.error("Settings file is encrypted. Cannot proceed!!")
                                else:
                                    log.error("Settings provided in an incorrect data format. Cannot proceed!!")

        except Exception as e:
            log.error(e, exc_info=True)

    def load_display_components(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading Display Components..")
            if self._constants_file_location is not None:
                if os.path.exists(self._constants_file_location):
                    with open(self._constants_file_location,"r") as f:
                        self._display_components = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def load_charts(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading Charts..")
            if self._constants_file_location is not None:
                if os.path.exists(self._constants_file_location):
                    with open(self._constants_file_location,"r") as f:
                        self._charts = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def load_constants(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading constants..")
            if self._constants_file_location is not None:
                if os.path.exists(self._constants_file_location):
                    with open(self._constants_file_location,"r") as f:
                        self._constants = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def load_messages(self):
        try:
            log = logging.getLogger("main")
            log.info("Loading Messages..")
            if self._messages_file_location is not None:
                if os.path.exists(self._messages_file_location):
                    with open(self._messages_file_location, "r") as f:
                        self._messages = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def load_master(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading Master..")
            if self._master_file_location is not None:
                if os.path.exists(self._master_file_location):
                    with open(self._master_file_location, "r") as f:
                        self._master = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def load_lookups(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading Lookups..")
            if self._lookups_file_location is not None:
                if os.path.exists(self._lookups_file_location):
                    with open(self._lookups_file_location, "r") as f:
                        self._lookups = json.load(f)
        except Exception as e:
            log.error(e, exc_info=True)

    def get_constants(self):
        return self._constants

    def get_lookups(self):
        return self._lookups

    def get_display_components(self):
        return self._display_components

    def get_charts(self):
        return self._charts

    def get_datalake_storage(self):
        return self._datalake_storage

    def get_calendar_datasets(self):
        return self._calendar_datasets