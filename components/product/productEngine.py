import logging
import json
import os
import sys
import logging
import json
import string
import os
import sys
import uuid
import random
import datetime
import socket
import platform
import secrets
from django.utils import timezone

from components.product.modules.settings import Settings

class ProductEngine:

    _secret_key = "18fe008f-afce-4a2d-a43e-397d1b41148a"
    _namespace_url = 'http://www.adventbizsolutions.com/adbiz/namespace'

    constants = {}
    lookups = {}

    _masters = {}
    #_product_instance_id = ""
    _root_namespace = ""
    _registered_to = ""
    _activation_file_location = ""
    _product_engine_code = ""
    _activation_key = ""
    _activation_dt = ""
    _host_name = ""
    _host_ip_address = ""
    _os_release = ""
    _release_info = ""
    


    def __init__(self, sf = "/home/setupadmin/adbiz/components/product/config/settings.json"):
        try:
            if os.path.exists (sf):

                print("Initializing Product Engine")
                print("Reading Settings File")
                productSettings = Settings(sf)
                log = productSettings.get_loggger()
                self.constants = productSettings.get_constants()
                self.lookups = productSettings.get_lookups()
                masterData = productSettings.get_masters()
                self._root_namespace = masterData["namespace"]["root"]
                self._activation_file_location = productSettings.get_activation_file()
                self._release_file_location = productSettings.get_release_info()

                if os.path.exists(self._activation_file_location):
                    with open(self._activation_file_location, "r") as f:
                        data = json.load(f)
                        print(data["activationKey"])
            else:
                print("Error!! Settings file not found. Cannot initialize Product Engine.")

        except Exception as e:
            msg = "Error in initializing Product Engine!!" + str(e)
            log.error(msg)

    # activate the product by providing the payload. Payload is descrypted, validated and a unique key is created
    # matches the secret key from the payload to the one configured in the master settings
    def activate_product_engine(self, payload):
        try:
            log = logging.getLogger(__name__)
            log.info("Product activation initiated...")
            if os.path.exists(self._activation_file_location):
                log.error("Error!! Activation file already exists. Please delete the file and proceed to reactivate..")
            else:
                if self._validate_payload(payload):
                    payload_key = payload["secret_key"]
                    if payload_key == self._secret_key:
                        self._registered_to = payload["registered_to"]
                        self._activation_dt = str(timezone.now())
                        self._product_engine_code = str(uuid.uuid4())  #secrets.token_hex(10) + "@" + self._root_namespace
                        self._activation_key = str(uuid.uuid5(uuid.NAMESPACE_URL, self._namespace_url))
                        if platform.system() == 'Linux' or platform.system() == 'Linux2':
                            self._host_name = socket.gethostname()
                            self._host_ip_address = socket.gethostbyname(self._host_name)
                            self._os_release = platform.release()
                        elif platform.system() == 'Windows':
                            self._host_name = os.environ['COMPUTERNAME']
                            self._host_ip_address = socket.gethostname(self._host_name)
                            self._os_release = platform.release()

                        log.info(payload)
                        data = self._create_activation_file()
                        if data:
                            log.info("Activation file created successfully!!")
                            log.info("Saving Activation details...")
                            return data
                        else:
                            log.error("Error!! Error in creating activation file.")

                else:
                    log.error("Error in Validating payload!!")

        except Exception as e:
            msg = "Error in activating the Product Engine!!" + str(e)
            log.error(msg)


    # todo: validate the submitted payload for activation
    def _validate_payload(self,input):
        try:
            log = logging.getLogger(__name__)
            print('Validating Payload..')
            return True
        except Exception as e:
            msg = "Error in the payload format. Please modify and submit again!!" + str(e)
            log.error(msg)

    def _create_activation_file(self):
        try:
            log = logging.getLogger(__name__)
            log.info("Creating Activation file...")
            data = dict(registered_to=self._registered_to, activation_dt=self._activation_dt,
                        activation_key=self._activation_key, engine_id=self._product_engine_code, host_name=self._host_name, release_info=self._release_info,os_release=self._os_release,
                        host_ip_address=self._host_ip_address, activation_file_location = self._activation_file_location)
            print(data)
            f = open(self._activation_file_location, "w+")
            f.write(json.dumps(data))
            log.info("Activation file successfully created !!")
            return data
        except Exception as e:
            msg = "Error in creating activation file!!" + str(e)
            log.error(msg)


    def get_root_namespace(self):
        return self._root_namespace

    def get_activation_file_location(self):
        return self._activation_file_location


    def add_customer(self, payload):
        try:
            log = logging.getLogger(__name__)
            log.info("Creating new Customer...")
            uq = random.randrange(10**11, 10**12)
            ns = payload["customer_namespace"]
            pe = payload["engine_id"]
            customer_id = str(uq) + "@" + str(ns)
            reg = payload["registration_number"]
            reg_dt = payload["registration_dt"]


        except Exception as e:
            msg = "Error in creating new Customer!!" + str(e)
            log.error(msg)