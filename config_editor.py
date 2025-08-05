#!/usr/bin/env python3
"""
Simple web server to edit config.json file.
Provides a web interface to modify configuration settings.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import sys

app = Flask(__name__)

# Configuration file path
CONFIG_FILE = 'config.json'

# Default configuration structure based on setupconfig.py
DEFAULT_CONFIG = {
    "classID": "0",
    "color-scheme": {
        "primary": "1",
        "cancelled": "11",
        "changed": "5",
        "exam": "10"
    },
    "weeksAhead": 3,
    "maintenance": False,
    "showCancelled": False,
    "showChanges": False
}

def load_config():
    """Load config from file or create with defaults if it doesn't exist."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config_data):
    """Save config to file."""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False

@app.route('/')
def index():
    """Main configuration page."""
    config = load_config()
    return render_template('config_editor.html', config=config)

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration as JSON."""
    config = load_config()
    return jsonify(config)

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration from JSON data."""
    try:
        new_config = request.get_json()
        
        # Validate required fields
        if 'classID' not in new_config:
            return jsonify({'error': 'classID is required'}), 400
        
        # Ensure color-scheme exists and has required fields
        if 'color-scheme' not in new_config:
            new_config['color-scheme'] = DEFAULT_CONFIG['color-scheme'].copy()
        
        color_scheme = new_config['color-scheme']
        for color_key in ['primary', 'cancelled', 'changed', 'exam']:
            if color_key not in color_scheme:
                color_scheme[color_key] = DEFAULT_CONFIG['color-scheme'][color_key]
        
        # Set defaults for missing fields
        for key, default_value in DEFAULT_CONFIG.items():
            if key not in new_config and key != 'color-scheme':
                new_config[key] = default_value
        
        # Save the configuration
        if save_config(new_config):
            return jsonify({'success': True, 'message': 'Configuration saved successfully'})
        else:
            return jsonify({'error': 'Failed to save configuration'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Invalid configuration data: {str(e)}'}), 400

@app.route('/reset', methods=['POST'])
def reset_config():
    """Reset configuration to defaults."""
    if save_config(DEFAULT_CONFIG.copy()):
        return redirect(url_for('index'))
    else:
        return "Error resetting configuration", 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Check if template exists, create it if not
    template_path = 'templates/config_editor.html'
    if not os.path.exists(template_path):
        print("Creating HTML template...")
        # Create the template (see next file creation)
    
    print("Starting config editor web server...")
    print("Open http://localhost:5000 in your browser to edit config.json")
    print("Press Ctrl+C to stop the server")
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
