import configparser
from datetime import timedelta, datetime

cfg = configparser.ConfigParser()
cfg.read('app/config.cfg')

class Config():
    APP_NAME = cfg['app']['name']
    SECRET_KEY = cfg['app']['secret_key']

    if cfg['mysql']['log_queries'].upper() == 'TRUE':
        log_query = True
    else:
        log_query = False

    if cfg['app']['web_enable'].upper() == 'TRUE':
        WEB_ENABLE = True
    else:
        WEB_ENABLE = False
    
    if cfg['app']['api_enable'].upper() == 'TRUE':
        API_ENABLE = True
    else:
        API_ENABLE = False

    MASTER_DATABASE = {
        'driver': 'mysql',
        'host': cfg['mysql']['host'],
        'database': cfg['mysql']['db'],
        'user': cfg['mysql']['user'],
        'password': cfg['mysql']['password'],
        'prefix': cfg['mysql']['prefix'],
        'log_queries': True
    }
    SLAVE_DATABASE = {
        'driver': 'mysql',
        'host': cfg['mysql_slave']['host'],
        'database': cfg['mysql_slave']['db'],
        'user': cfg['mysql_slave']['user'],
        'password': cfg['mysql_slave']['password'],
        'prefix': cfg['mysql_slave']['prefix'],
        'log_queries': True
    }
    SLAVE_EXPORT_DATABASE = {
        'driver': 'mysql',
        'host': cfg['mysql_slave_export']['host'],
        'database': cfg['mysql_slave_export']['db'],
        'user': cfg['mysql_slave_export']['user'],
        'password': cfg['mysql_slave_export']['password'],
        'prefix': cfg['mysql_slave_export']['prefix'],
        'log_queries': True
    }
    ORATOR_DATABASES = {
        'default': 'master',
        'master': MASTER_DATABASE,
        'slave': SLAVE_DATABASE,
        'slave_export': SLAVE_EXPORT_DATABASE
    }

    if 'unix_socket' in cfg['mysql']:
        ORATOR_DATABASES['mysql']['unix_socket'] = cfg['mysql']['unix_socket']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
