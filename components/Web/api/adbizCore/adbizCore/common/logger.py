from logging.config import dictConfig
import logging
import logging.handlers
import os
import json, sys

logger = logging.getLogger(__name__)

class Adbizlogger:

    _custom_log_config_file = ""
    _base_log_folder = ""
    _config = {}

    def __init__(self, base_log_folder, log_config_file):
        try:

            if os.path.exists(base_log_folder):
                self._base_log_folder = base_log_folder
                print("Reading Logging Configuration File")
                if log_config_file is not None:
                    if os.path.exists(log_config_file):
                        self._custom_log_config_file = log_config_file
                        self.configure_logging()
                    else:
                        print("Error!! Logging Config path incorrect!!!")
                        sys.exit()
                else:
                    pass
                    # to do: use default configurations
            else:
                print("Error!!! Base log folder doesnt exists..", base_log_folder)
                sys.exit()

        except Exception as e:
            print("Error initializing Logger for Core Engine!!")
            print(str(e))
            sys.exit()

    def configure_logging(self):
        """
        Initialize logging defaults for Project.

        :param logfile_path: logfile used to the logfile
        :type logfile_path: string

        This function does:

        - Assign INFO and DEBUG level to logger file handler and console handler

        """
        try:
            print("Configuring Logging..")

            with open(self._custom_log_config_file, "r") as f:
                config = json.load(f)

            dictConfig(config["LOGGING"])
            print("Logging file initialized!!!")
            return True

        except Exception as e:
            print("Error in Loading Log config settings!!", e)
            return False



