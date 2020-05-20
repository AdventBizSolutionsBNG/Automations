class FlatFileConnector:

    _folder_path = ""
    _folder_path_pattern = ""
    _file_name = ""
    _file_name_pattern = ""
    _file_extn = []
    _separator = ""
    _max_file_sizeMb = 0
    _is_zipped = False
    _is_password = False
    _password = ""
    _error_folder_path = ""
    _is_archive = True
    _archive_folder_path = ""
    _start_row = 0
    _end_row = 0
    _is_encrypted =  False
    _encryption_type = ""
    _ignore_header_row = True

    def __init__(self):
        try:
            pass
        except Exception as e:
            print(e)

