from enum import Enum




######################################
# 
# Logging
#
######################################

class logLevel(Enum):
    ERROR = "ERR"
    WARNING = "WRN"
    INFO = "INF"

######################################
# 
# Config
#
######################################

class cfgParams(Enum):
    CLASSID="classID"
    COLORSCHEME="color-scheme"
    PRIMARYCOLOR="primary"
    CANCELLEDCOLOR="cancelled"
    CHANGEDCOLOR="changed"
    EXAMCOLOR="exam"
    WEEKSAHEAD="weeksAhead"
    MAINTENANCE="maintenance"
    SHOWCANCELLED="showCancelled"
    SHOWCHANGES="showChanges"
    HISTORY="history"
    
class envFile(Enum):
    CALENDARID="calendarID"
    COOKIE="cookie"
    SCHOOL="anonymous-school"
    BOTTOKEN="telegramToken"
    CHAT="telegramChat"
    
class credsParams(Enum):
    TYPE="type"
    PROJECT="project_id"
    PRIVATEKEYID="private_key_id"
    PRIVATEKEY="private_key"
    EMAIL="client_email"
    CLIENTID="client_id"
    URIAUTH="auth_uri"
    URITOKEN="token_uri"
    CERTPROVIDER="auth_provider_x509_cert_url"
    CERTCLIENT="client_x509_cert_url"
    DOMAIN="universe_domain"

######################################
# 
# Environment
#
######################################

class envParams(Enum):
    CLASSID= "CLASS_ID"
    PRIMARYCOLOR= "COLOR_PRIMARY"
    CANCELLEDCOLOR="COLOR_CANCELLED"
    CHANGEDCOLOR="COLOR_CHANGED"
    EXAMCOLOR="COLOR_EXAM"
    WEEKSAHEAD="WEEKS_AHEAD"
    MAINTENANCE="MAINTENANCE"
    SHOWCANCELLED="SHOW_CANCELLED"
    SHOWCHANGED="SHOW_CHANGES"
    HISTORY="HISTORY_COUNT"

######################################
# 
# MISC
#
######################################

class mapBoolean(Enum):
    "true" = True
    "1" = True
    "yes" = True
    "on" = True
    "false" = False
    "0" = False
    "no" = False
    "off" = False

######################################
# 
# Files
#
######################################

class files(Enum):
    CONFIG = 'config.json'
    CREDENTIALS = 'credentials.json'
    ENVIRONMENT = 'environment.json'
   