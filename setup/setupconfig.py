#!/usr/bin/env python3
"""
Script to generate config.json from environment variables.
If environment variables are not set, default values will be used.
"""

import os
import json
import sys

DEFAULTCLASSID=0
DEFAULTPRIMARY=1
DEFAULTCANCELLED=11
DEFAULTCHANGED=5
DEFAULTEXAM=10
DEFAULTWEEKSAHEAD=3
DEFAULTMAINTENANCE=False
DEFAULTSHOWCANCELLED=False
DEFAULTSHOWCHANGES=False
DEFAULTMAXBATCH=4032
ENVCLASSID= "CLASS_ID"
ENVPRIMARYCOLOR= "COLOR_PRIMARY"
ENVCANCELLEDCOLOR="COLOR_CANCELLED"
ENVCHANGEDCOLOR="COLOR_CHANGED"
ENVEXAMCOLOR="COLOR_EXAM"
ENVWEEKSAHEAD="WEEKS_AHEAD"
ENVMAINTENANCE="MAINTENANCE"
ENVSHOWCANCELLED="SHOW_CANCELLED"
ENVSHOWCHANGED="SHOW_CHANGES"
ENVMAXBATCH="MAX_BATCH"
CFGCLASSID="classID"
CFGCOLORSCHEME="color-scheme"
CFGPRIMARYCOLOR="primary"
CFGCANCELLEDCOLOR="cancelled"
CFGCHANGEDCOLOR="changed"
CFGEXAMCOLOR="exam"
CFGWEEKSAHEAD="weeksAhead"
CFGMAINTENANCE="maintenance"
CFGSHOWCANCELLED="showCancelled"
CFGSHOWCHANGES="showChanges"
CFGMAXBATCH="maxBatch"


def get_env_or_default(env_var, default_value, value_type=str):
    """
    Get environment variable value or return default if not set or empty.
    
    Args:
        env_var (str): Environment variable name
        default_value: Default value to use if env var is not set
        value_type: Type to convert the value to (str, int, float, bool)
    
    Returns:
        Converted value or default
    """
    value = os.environ.get(env_var, '').strip()
    if not value:
        return default_value
    
    try:
        if value_type == bool:
            # Handle boolean conversion from string
            if value.lower() in ('true', '1', 'yes', 'on'):
                return True
            elif value.lower() in ('false', '0', 'no', 'off'):
                return False
            else:
                print(f"[WRN] Invalid boolean value '{value}' for {env_var}, using default: {default_value}")
                return default_value
        elif value_type == int:
            return int(value)
        elif value_type == float:
            return float(value)
        else:
            return value
    except ValueError:
        print(f"[WRN] Invalid value '{value}' for {env_var}, using default: {default_value}")
        return default_value


def create_config():
    """Create config.json from environment variables with defaults."""
    
    # Read environment variables with defaults based on the template
    config = {
        CFGCLASSID: get_env_or_default(ENVCLASSID, f"{DEFAULTCLASSID}"),
        CFGCOLORSCHEME: {
            CFGPRIMARYCOLOR: get_env_or_default(ENVPRIMARYCOLOR, f"{DEFAULTPRIMARY}"),
            CFGCANCELLEDCOLOR: get_env_or_default(ENVCANCELLEDCOLOR, f"{DEFAULTCANCELLED}"),
            CFGCHANGEDCOLOR: get_env_or_default(ENVCHANGEDCOLOR, f"{DEFAULTCHANGED}"),
            CFGEXAMCOLOR: get_env_or_default(ENVEXAMCOLOR, f"{DEFAULTEXAM}")
        },
        CFGWEEKSAHEAD: get_env_or_default(ENVWEEKSAHEAD, DEFAULTWEEKSAHEAD, int),
        CFGMAINTENANCE: get_env_or_default(ENVMAINTENANCE, DEFAULTMAINTENANCE, bool),
        CFGSHOWCANCELLED: get_env_or_default(ENVSHOWCANCELLED, DEFAULTSHOWCANCELLED, bool),
        CFGSHOWCHANGES: get_env_or_default(ENVSHOWCHANGED, DEFAULTSHOWCHANGES, bool),
        CFGMAXBATCH: get_env_or_default(ENVMAXBATCH, DEFAULTMAXBATCH, int)
        }
    
    return config

def create_env():
    env = {
      "calendarID": "",
      "cookie": "",
      "anonymous-school": "",
      "telegramToken": "",
      "telegramChat": ""
    }
    return env

def create_creds():
    creds = {
      "type": "",
      "project_id": "",
      "private_key_id": "",
      "private_key": "",
      "client_email": "",
      "client_id": "",
      "auth_uri": "",
      "token_uri": "",
      "auth_provider_x509_cert_url": "",
      "client_x509_cert_url": "",
      "universe_domain": ""
    }
    return creds


def main():
    """Main function to generate config.json file."""
    try:
        # Create config dictionary
        config = create_config()
        creds = create_creds()
        envs = create_env()
        
        # Write to config.json file
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        creds_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
        envs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'environment.json')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
            
        with open(creds_path, 'w', encoding='utf-8') as f:
            json.dump(creds, f, indent=2, ensure_ascii=False)
            
        with open(envs_path, 'w', encoding='utf-8') as f:
            json.dump(envs, f, indent=2, ensure_ascii=False)
        
        print(f"[INF] Config file created successfully at: {config_path}")
        print("[INF] Configuration:")
        for line in json.dumps(config, indent=2).split('\n'):
            print(f"[INF] {line}")
        
        # Print environment variables that were used
        print("[INF] Environment variables used:")
        env_vars = [
            (ENVCLASSID, config[CFGCLASSID]),
            (ENVPRIMARYCOLOR, config[CFGCOLORSCHEME][CFGPRIMARYCOLOR]),
            (ENVCANCELLEDCOLOR, config[CFGCOLORSCHEME][CFGCANCELLEDCOLOR]),
            (ENVCHANGEDCOLOR, config[CFGCOLORSCHEME][CFGCHANGEDCOLOR]),
            (ENVEXAMCOLOR, config[CFGCOLORSCHEME][CFGEXAMCOLOR]),
            (ENVWEEKSAHEAD, config[CFGWEEKSAHEAD]),
            (ENVMAINTENANCE, config[CFGMAINTENANCE]),
            (ENVSHOWCANCELLED, config[CFGSHOWCANCELLED]),
            (ENVSHOWCHANGED, config[CFGSHOWCHANGES]),
            (ENVMAXBATCH, config[CFGMAXBATCH])
        ]
        
        for env_var, value in env_vars:
            env_value = os.environ.get(env_var, '').strip()
            if env_value:
                print(f"[INF]  {env_var}={env_value} ✓")
            else:
                print(f"[INF]  {env_var}=(not set, using default: {value})")
                
    except Exception as e:
        print(f"[ERR] Error creating config file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()