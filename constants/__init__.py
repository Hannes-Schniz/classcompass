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
    CLASSID = "classID"
    COLORSCHEME = "color-scheme"
    PRIMARYCOLOR = "primary"
    CANCELLEDCOLOR = "cancelled"
    CHANGEDCOLOR = "changed"
    EXAMCOLOR = "exam"
    WEEKSAHEAD = "weeksAhead"
    MAINTENANCE = "maintenance"
    SHOWCANCELLED = "showCancelled"
    SHOWCHANGED = "showChanged"
    MAXBATCH = "maxBatch"


class envFile(Enum):
    CALENDARID = "calendarID"
    COOKIE = "cookie"
    SCHOOL = "anonymous-school"
    BOTTOKEN = "telegramToken"
    CHAT = "telegramChat"


class credsParams(Enum):
    TYPE = "type"
    PROJECT = "project_id"
    PRIVATEKEYID = "private_key_id"
    PRIVATEKEY = "private_key"
    EMAIL = "client_email"
    CLIENTID = "client_id"
    URIAUTH = "auth_uri"
    URITOKEN = "token_uri"
    CERTPROVIDER = "auth_provider_x509_cert_url"
    CERTCLIENT = "client_x509_cert_url"
    DOMAIN = "universe_domain"


######################################
#
# Database
#
######################################


class dbParams(Enum):
    SQLDIRVAR = "SQL_DIR"
    DBPATHVAR = "DB_PATH"
    DBPATHDEF = "/classcompass-db/maps.db"
    CREATECLASSESSQLFILE = "createClasses.sql"
    CREATENOTIFICATIONFILE = "createNotification.sql"
    CREATEDIFFSQLFILE = "createDiff.sql"
    CLASSESTABLE = "classes"
    DIFFTABLE = "diff"


######################################
#
# Environment
#
######################################


class envParams(Enum):
    CLASSID = "CLASS_ID"
    PRIMARYCOLOR = "COLOR_PRIMARY"
    CANCELLEDCOLOR = "COLOR_CANCELLED"
    CHANGEDCOLOR = "COLOR_CHANGED"
    EXAMCOLOR = "COLOR_EXAM"
    WEEKSAHEAD = "WEEKS_AHEAD"
    MAINTENANCE = "MAINTENANCE"
    SHOWCANCELLED = "SHOW_CANCELLED"
    SHOWCHANGED = "SHOW_CHANGED"
    MAXBATCH = "MAX_BATCH"


######################################
#
# MISC
#
######################################

mapBoolean = {
    "true": True,
    "1": True,
    "yes": True,
    "on": True,
    "false": False,
    "0": False,
    "no": False,
    "off": False,
}

######################################
#
# Files
#
######################################


class files(Enum):
    CONFIG = "/classcompass-cfg/config.json"
    CREDENTIALS = "/classcompass-cfg/credentials.json"
    ENVIRONMENT = "/classcompass-cfg/environment.json"


######################################
#
# API
#
######################################


class api(Enum):
    DATE = "date"
    STARTTIME = "startTime"
    ENDTIME = "endTime"
    TYPE = "type"
    STATE = "state"
    STATEDETAIL = "stateDetail"
    ROOM = "room"
    SUBJECT = "subject"
    SUBSTITUTETEXT = "substituteText"
    OLDDATE = "oldDate"
    NEWDATE = "newDate"
    OLDSTART = "oldStart"
    NEWSTART = "newStart"
    OLDEND = "oldEnd"
    NEWEND = "newEnd"
    OLDSTATE = "oldState"
    NEWSTATE = "newState"
    OLDSTATEDETAIL = "oldStateDetail"
    NEWSTATEDETAIL = "newStateDetail"
    OLDROOM = "oldRoom"
    NEWROOM = "newRoom"
    OLDSUBJECT = "oldSubject"
    NEWSUBJECT = "newSubject"
    OLDTEXT = "oldText"
    NEWTEXT = "newText"
