#!/usr/bin/env python3
"""
Script to generate config.json from environment variables.
If environment variables are not set, default values will be used.
"""

import os
import json
import sys
from constants import cfgParams, envParams, envFile, credsParams, mapBoolean, logLevel


DEFAULTCLASSID=0
DEFAULTPRIMARY=1
DEFAULTCANCELLED=11
DEFAULTCHANGED=5
DEFAULTEXAM=10
DEFAULTWEEKSAHEAD=3
DEFAULTMAINTENANCE=False
DEFAULTSHOWCANCELLED=False
DEFAULTSHOWCHANGES=False
DEFAULTHISTORY=2016


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
            try:
                return mapBoolean[value.lower()]
            except:
                print(f"[{logLevel.WARNING.value}] Invalid boolean value '{value}' for {env_var}, using default: {default_value}")
                return default_value 


        elif value_type == int:
            return int(value)
        elif value_type == float:
            return float(value)
        else:
            return value
    except ValueError:
        print(f"[{logLevel.WARNING.value}]] Invalid value '{value}' for {env_var}, using default: {default_value}")
        return default_value


def create_config():
    """Create config.json from environment variables with defaults."""
    
    # Read environment variables with defaults based on the template
    config = {
        cfgParams.CLASSID.value: get_env_or_default(envParams.CLASSID.value, f"{DEFAULTCLASSID}"),
        cfgParams.COLORSCHEME.value: {
            cfgParams.PRIMARYCOLOR.value: get_env_or_default(envParams.PRIMARYCOLOR.value, f"{DEFAULTPRIMARY}"),
            cfgParams.CANCELLEDCOLOR.value: get_env_or_default(envParams.CANCELLEDCOLOR.value, f"{DEFAULTCANCELLED}"),
            cfgParams.CHANGEDCOLOR.value: get_env_or_default(envParams.CHANGEDCOLOR.value, f"{DEFAULTCHANGED}"),
            cfgParams.EXAMCOLOR.value: get_env_or_default(envParams.EXAMCOLOR.value, f"{DEFAULTEXAM}")
        },
        cfgParams.WEEKSAHEAD.value: get_env_or_default(envParams.WEEKSAHEAD.value, DEFAULTWEEKSAHEAD, int),
        cfgParams.MAINTENANCE.value: get_env_or_default(envParams.MAINTENANCE.value, DEFAULTMAINTENANCE, bool),
        cfgParams.SHOWCANCELLED.value: get_env_or_default(envParams.SHOWCANCELLED.value, DEFAULTSHOWCANCELLED, bool),
        cfgParams.SHOWCHANGES.value: get_env_or_default(envParams.SHOWCHANGED.value, DEFAULTSHOWCHANGES, bool),
        cfgParams.HISTORY.value: get_env_or_default(envParams.HISTORY.value, DEFAULTSHOWCHANGES, bool)
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
            (envParams.CLASSID.value, config[cfgParams.CLASSID.value]),
            (envParams.PRIMARYCOLOR.value, config[cfgParams.COLORSCHEME.value][cfgParams.PRIMARYCOLOR.value]),
            (envParams.CANCELLEDCOLOR.value, config[cfgParams.COLORSCHEME.value][cfgParams.]),
            (envParams.CHANGEDCOLOR.value, config[cfgParams.COLORSCHEME.value][CFGCHANGEDCOLOR]),
            (envParams.EXAMCOLOR.value, config[cfgParams.COLORSCHEME.value][CFGEXAMCOLOR]),
            (envParams.WEEKSAHEAD.value, config[CFGWEEKSAHEAD]),
            (envParams.MAINTENANCE.value, config[CFGMAINTENANCE]),
            (envParams.SHOWCANCELLED.value, config[CFGSHOWCANCELLED]),
            (envParams.SHOWCHANGED.value, config[CFGSHOWCHANGES]),
            (envParams.HISTORY.value, config[CFGHISTORY])

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
