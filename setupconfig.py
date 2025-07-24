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
                print(f"Warning: Invalid boolean value '{value}' for {env_var}, using default: {default_value}")
                return default_value
        elif value_type == int:
            return int(value)
        elif value_type == float:
            return float(value)
        else:
            return value
    except ValueError:
        print(f"Warning: Invalid value '{value}' for {env_var}, using default: {default_value}")
        return default_value


def create_config():
    """Create config.json from environment variables with defaults."""
    
    # Read environment variables with defaults based on the template
    config = {
        "classID": get_env_or_default("CLASS_ID", f"{DEFAULTCLASSID}"),
        "color-scheme": {
            "primary": get_env_or_default("COLOR_PRIMARY", f"{DEFAULTPRIMARY}"),
            "cancelled": get_env_or_default("COLOR_CANCELLED", f"{DEFAULTCANCELLED}"),
            "changed": get_env_or_default("COLOR_CHANGED", f"{DEFAULTCHANGED}"),
            "exam": get_env_or_default("COLOR_EXAM", f"{DEFAULTEXAM}")
        },
        "weeksAhead": get_env_or_default("WEEKS_AHEAD", DEFAULTWEEKSAHEAD, int),
        "maintenance": get_env_or_default("MAINTENANCE", DEFAULTMAINTENANCE, bool),
        "showCancelled": get_env_or_default("SHOW_CANCELLED", DEFAULTSHOWCANCELLED, bool),
        "showChanges": get_env_or_default("SHOW_CHANGES", DEFAULTSHOWCHANGES, bool)
        }
    
    return config


def main():
    """Main function to generate config.json file."""
    try:
        # Create config dictionary
        config = create_config()
        
        # Write to config.json file
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Config file created successfully at: {config_path}")
        print("Configuration:")
        print(json.dumps(config, indent=2))
        
        # Print environment variables that were used
        print("\nEnvironment variables used:")
        env_vars = [
            ("CLASS_ID", config["classID"]),
            ("COLOR_PRIMARY", config["color-scheme"]["primary"]),
            ("COLOR_CANCELLED", config["color-scheme"]["cancelled"]),
            ("COLOR_CHANGED", config["color-scheme"]["changed"]),
            ("COLOR_EXAM", config["color-scheme"]["exam"]),
            ("WEEKS_AHEAD", config["weeksAhead"]),
            ("MAINTENANCE", config["maintenance"]),
            ("SHOW_CANCELLED", config["showCancelled"]),
            ("SHOW_CHANGES", config["showChanges"])
        ]
        
        for env_var, value in env_vars:
            env_value = os.environ.get(env_var, '').strip()
            if env_value:
                print(f"  {env_var}={env_value} ✓")
            else:
                print(f"  {env_var}=(not set, using default: {value})")
                
    except Exception as e:
        print(f"❌ Error creating config file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()