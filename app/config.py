import configparser
from datetime import timedelta, datetime

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

class Config():
    APP_NAME = cfg['app']['name']
    SECRET_KEY = cfg['app']['secret_key']
    MAX_LOGIN_ATTEMPT = cfg['app']['max_login_attempt']

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

    # CACHE
    CACHE_KEY_PREFIX = cfg['cache']['prefix']
    CACHE_REDIS_HOST = cfg['redis']['host']
    CACHE_REDIS_PORT = cfg['redis']['port']
    CACHE_DEFAULT_TIMEOUT = cfg['cache']['timeout']

    # JWT
    JWT_SECRET_KEY = cfg['jwt']['secret']
    JWT_ALGORITHM = cfg['jwt']['algo']
    jwt_auth_expired_use_default= False

    jwt_config_act={}
    jwt_config_rte={}
    timedelta_units=['weeks','days','hours','minutes','seconds','microseconds']

    if 'token_access_exp_unit' in cfg['jwt'] and cfg['jwt']['token_access_exp_unit'] in timedelta_units:
        jwt_config_act[cfg['jwt']['token_access_exp_unit']]=int(cfg['jwt']['token_exp'])
    else:
        jwt_config_act['days']=int(cfg['jwt']['token_exp'])

    if 'token_refresh_exp_unit' in cfg['jwt'] and cfg['jwt']['token_refresh_exp_unit'] in timedelta_units:
        jwt_config_rte[cfg['jwt']['token_refresh_exp_unit']]=int(cfg['jwt']['refresh_exp'])
    else:
        jwt_config_rte['days']=int(cfg['jwt']['refresh_exp'])

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(**jwt_config_act)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(**jwt_config_rte)


class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
