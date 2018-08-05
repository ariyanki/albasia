import configparser
from datetime import timedelta, datetime

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Config():
    APP_NAME = cfg['app']['name']
    SECRET_KEY = cfg['app']['secret_key']

    if cfg['mysql']['log_queries'].upper() == 'TRUE':
        LOG_QUERY = True
    else:
        LOG_QUERY = False

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
        'log_queries': LOG_QUERY
    }
    
    ORATOR_DATABASES = {
        'default': 'master',
        'master': MASTER_DATABASE
    }

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
