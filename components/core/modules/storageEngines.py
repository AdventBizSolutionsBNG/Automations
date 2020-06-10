

class DataLakeStorage:
    _engine_type = ""
    _engine_sub_type = ""
    _target_host_name = ""
    _user = ""
    _password = ""
    _access_key = ""
    _port = ""
    _reference_class = ""

    def __init__(self, config):
        try:
            self._engine_type = config["engine_type"]
            self._engine_sub_type = config["engine_sub_type"]
            self._target_host_name = config["target_host_name"]
            self._user = config["user"]
            self._password = config["password"]
            self._access_key = config["access_key"]
            self._port = config["port"]
            self._reference_class = config["reference_class"]

            if self.validate_connection():
                print("Successfully connected to Data lake storage system!!")
        except Exception as e:
            print("Error in setting up Data lake Storage Engine!!", e)

    def get_data_lake_engine_type(self):
        return self._engine_type

    def get_data_lake_engine_sub_type(self):
        return self._engine_sub_type

    def get_data_lake_user(self):
        return self._user

    def get_data_lake_password(self):
        return self._password

    def get_data_lake_port(self):
        return self._port

    def get_data_lake_engine_class(self):
        return self._reference_class

    # validate the settings by connecting to the target storage system on init
    def validate_connection(self):
        try:
            return True
        except Exception as e:
            print(e)
            return False