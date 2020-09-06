import logging
import json
import os
import sys
import socket
import platform
import random
import uuid
from django.utils import timezone
from components.core.modules.settings import Settings


class CoreEngine:
    _secret_key = '2wu@9s(ks=n5nz113-vnhf6)sf9ud)u!fods5z96**sf91o48$'
    _namespace_url = 'http://www.adventbizsolutions.com/adbiz/namespace'


    constants = {}
    lookups = {}
    components = {}
    charts = {}
    calendars = []

    _core_engine_code = ""
    _product_engine_url = ""
    _product_engine_code = ""
    _customer_code = ""
    _customer_namespace = ""
    _registered_to = ""
    _activation_file_location = ""
    _activation_key = ""
    _activation_dt = ""
    _host_name = ""
    _host_ip_address = ""
    _os_release = ""
    _release_info = ""
    _validity_start_date = ""
    _validity_end_date = ""
    _is_activated = ""

    def __init__(self, sf = "/home/setupadmin/adbiz/components/core/config/settings.json"):
        try:
            if os.path.exists (sf):
                print("Initializing Core Engine")
                print("Reading Settings File")
                coreSettings = Settings(sf)
                self.components = coreSettings.get_display_components()
                self.constants = coreSettings.get_constants()
                self.lookups = coreSettings.get_lookups()
                self.calendars = coreSettings.get_calendar_datasets()
            else:
                print("Error!! Settings file not found. Cannot initialize Core Engine.")
        except Exception as e:
            print("Error in initializing Core Engine!!")
            print(e)

    # activate the core by providing the payload. Payload is descrypted, validated and a unique key is created
    # matches the secret key from the payload to the one configured in the master settings (todo)
    def activate_core_engine(self, payload):
        try:
            log = logging.getLogger(__name__)
            log.info("Core activation initiated...")
            if os.path.exists(self._activation_file_location):
                log.error(
                    "Error!! Activation file already exists. Please delete the file and proceed to reactivate..")
            else:
                if self._validate_payload(payload):
                    payload_key = payload["secret_key"]
                    product_sync_url = payload["product_sync_url"]
                    if payload_key == self._secret_key:
                        self._registered_to = payload["registered_to"]
                        self._activation_dt = str(timezone.now())
                        self._engine_id = str(uuid.uuid4())  # secrets.token_hex(10) + "@" + self._root_namespace
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
            msg = "Error in activating the core Engine!!" + str(e)
            log.error(msg)

    # todo: validate the submitted payload for activation
    def _validate_payload(self, input):
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
                        activation_key=self._activation_key, engine_id=self._engine_id, host_name=self._host_name,
                        release_info=self._release_info, os_release=self._os_release,
                        host_ip_address=self._host_ip_address,
                        activation_file_location=self._activation_file_location)
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