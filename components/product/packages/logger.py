import sys
from logging.config import dictConfig


class Logger:

    def __init__(self, config):
        try:
            if len(config)>0:
                dictConfig(config)

        except Exception as e:
            print("Errror in initializing logging system!!")
            sys.exit()
