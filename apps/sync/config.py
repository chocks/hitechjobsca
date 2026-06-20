
import os
import traceback

CONFIG_FILE_PATH = '/etc/opt/jobs-download/'


class Config:
    def __init__(self, file_path=None):
        self.config_file = file_path + '.config' if file_path else CONFIG_FILE_PATH + '.config'
        self.db_host = os.environ.get('DB_HOST')
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_name = os.environ.get('DB_NAME')
        self.data_folder = os.environ.get('DATA_FOLDER')

        if not all([self.db_host, self.db_user, self.db_password, self.db_name, self.data_folder]):
            try:
                with open(self.config_file) as config_file_handle:
                    for config_property in config_file_handle:
                        configs = config_property.split('=')

                        if configs[0] == 'DB_HOST':
                            self.db_host = self.db_host or configs[1].rstrip('\n')
                        elif configs[0] == 'DB_NAME':
                            self.db_name = self.db_name or configs[1].rstrip('\n')
                        elif configs[0] == 'DB_USER':
                            self.db_user = self.db_user or configs[1].rstrip('\n')
                        elif configs[0] == 'DB_PASSWORD':
                            self.db_password = self.db_password or configs[1].rstrip('\n')
                        elif configs[0] == 'DATA_FOLDER':
                            self.data_folder = self.data_folder or configs[1].rstrip('\n')

            except:
                print('Cannot load config file')
                traceback.print_exc()

        if not self.data_folder:
            self.data_folder = './'

    def get_db_host(self):
        return self.db_host

    def get_db_name(self):
        return self.db_name

    def get_db_user(self):
        return self.db_user

    def get_db_password(self):
        return self.db_password

    def get_data_folder(self):
        return self.data_folder
