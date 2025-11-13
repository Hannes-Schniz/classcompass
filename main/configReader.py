import json
import re
from constants import cfgParams


class configExtract:
    conf = None
    def __init__(self, file):
        with open(file,"r") as conf:
           conf = json.load(conf)
        try:
            #self.configCheck(conf) 
            self.conf = conf
            #print(conf)
        except Exception as e:
            print(repr(e))
            raise Exception("Failed to load config")
        
           
           

    def configCheck(self,conf):
        if re.match(conf[cfgParams.CLASSID.value], "[0-9][0-9][0-9][0-9]") == None or len(conf[cfgParams.CLASSID.value]) != 4:
            raise Exception("No valid class ID configured")
        if re.match(conf[cfgParams.WEEKSAHEAD.value], "[0-9]") == None or len(conf[cfgParams.WEEKSAHEAD.value]) != 1:
            raise Exception("No valid weeks lookahead configured")
        
    