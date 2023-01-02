"""
    imports & globals
"""

import datetime
import os
from tools.convert import safe_cast


class AppConfiguration(object):
    """ configuraton class """

    _image = {}

    #
    #  Application Settings
    #
    PATH_LOG = ""
    LOG_FILE = "klax.log"
    LOG_LEVEL = 10 #debug
    TIMEZONE = "Europe/Berlin"
    CONTAINER_PATH_LOG = ""

    #
    # Database Configuration
    #
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_SCHEMA = 'klax'

    DATABASE_URI = ""

    #
    # Configure Datetime formats
    #
    DATEFORMAT = '%d.%m.%Y'
    DATETIMEFORMAT = '%d.%m.%Y %H:%M:%S'

    #
    # FAst Api Secret
    #
    SECRET = "SupaDupaSecret"

    def __init__(self):
        """ constructor """

        for key, default in vars(self.__class__).items():
            if not key.startswith('_') and key != '':
                if key in os.environ.keys():

                    value = os.environ.get(key)
                    to_type = type(default)

                    if to_type is datetime.datetime:
                        setattr(self, key, safe_cast(value, to_type, default, self._datetimeformat))

                    elif to_type is datetime.date:
                        setattr(self, key, safe_cast(value, to_type, default, self._dateformat))

                    else:
                        setattr(self, key, safe_cast(value, to_type, default))
                else:
                    setattr(self, key, default)

        # Custom Configuration part
        if self.CONTAINER_PATH_LOG != "" and self.CONTAINER_PATH_LOG:
            self.LOG_FILE = os.path.join(self.CONTAINER_PATH_LOG, self.LOG_FILE)
        else:
            self.LOG_FILE = os.path.join(self.PATH_LOG, self.LOG_FILE)

        if self.MYSQL_HOST != '' and self.MYSQL_HOST:
            #self.DATABASE_URI = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_HOST, self.MYSQL_SCHEMA)
            self.DATABASE_URI = "mysql://{0}:{1}@{2}:{3}/{4}".format(self.MYSQL_USER, self.MYSQL_PASSWORD, self.MYSQL_HOST, self.MYSQL_PORT, self.MYSQL_SCHEMA)
        else:

            self.DATABASE_URI = 'sqlite:///{0}'.format(os.path.join(self.PATH_LOG, self.MYSQL_SCHEMA))
        
        """ parse self into dictionary """

        

        for key, value in vars(self).items():
            if not key.startswith('_') and key != '':
                self._image[key] = value

    def __repr__(self):
        """ return config members to dictionary """
        return str(self._image)
