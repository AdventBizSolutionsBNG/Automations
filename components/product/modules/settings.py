import json
import os
import sys
import logging
from logging.config import dictConfig
from components.product.packages.logger import Logger

class Settings:
    _constants = {}
    _messages = {}
    _masters = {}
    _lookups = {}
    _logger = ""

    _constants_file_location = ""
    _messages_file_location = ""
    _masters_file_location = ""
    _lookups_file_location = ""
    _release_info_location = ""
    _activation_file_location = ""

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
                                log=logging.getLogger(__name__)
                                self._logger = log

            log.info("Initializing Core Engine Parameters..")
            with open(sfile, "r") as f:
                fdata = json.load(f)

            for k, v in fdata.items():
                if k == "releaseInfo":
                    self._release_info_location = v
                if k == "activationFile":
                    self._activation_file_location = v
                if k == "metaData":
                    for config in v:
                        for k1,v1 in config.items():
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
                            elif k1 == "masters":
                                if v1["type"] == "file":
                                    if v1["file"]["isEncrypted"] == "N":
                                        if v1["file"]["isPassword"] == "N":
                                            if v1["file"]["isZipped"] == "N":
                                                log.info("Reading Masters..")
                                                self._masters_file_location = v1["file"]["location"]
                                                self.load_masters()
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
            log.error(e)

    def load_constants(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading constants..")
            if self._constants_file_location is not None:
                if os.path.exists(self._constants_file_location):
                    with open(self._constants_file_location,"r") as f:
                        self._constants = json.load(f)
        except Exception as e:
            log.error(e)

    def load_messages(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading messages..")
            if self._constants_file_location is not None:
                if os.path.exists(self._messages_file_location):
                    with open(self._messages_file_location, "r") as f:
                        self._messages = json.load(f)
        except Exception as e:
            log.error(e)

    def load_masters(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading master..")
            if self._masters_file_location is not None:
                if os.path.exists(self._masters_file_location):
                    with open(self._masters_file_location, "r") as f:
                        self._masters = json.load(f)
        except Exception as e:
            log.error(e)

    def load_lookups(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Loading lookups..")
            if self._lookups_file_location is not None:
                if os.path.exists(self._lookups_file_location):
                    with open(self._lookups_file_location, "r") as f:
                        self._lookups = json.load(f)
        except Exception as e:
            log.error(e)

    def get_constants(self):
        return self._constants

    def get_lookups(self):
        return self._lookups

    def get_masters(self):
        return self._masters

    def get_release_info(self):
        return self._release_info_location

    def get_activation_file(self):
        return self._activation_file_location

    def get_loggger(self):
        return self._logger