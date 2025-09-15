#!/usr/bin/env python3
"""
ClassCompass Management Web GUI
Comprehensive Flask web application for managing ClassCompass configuration and database.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import sqlite3
import json
import os
import sys
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'classcompass-management-2025'

# Configuration file paths
CONFIG_FILE = '../config.json'
ENVIRONMENT_FILE = '../environment.json'

# Database path from environment variable
DB_PATH = os.environ.get('DB_PATH', '../maps.db')

# Default configurations
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

DEFAULT_ENVIRONMENT = {
    "calendarID": "",
    "cookie": "",
    "anonymous-school": "",
    "telegramToken": "",
    "telegramChat": ""
}

CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '../credentials.json')

# Utility Functions
def load_config():
    """Load config from file or create with defaults if it doesn't exist."""
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config_data):
    """Save config to file."""
    try:
        config_path = os.path.join(os.path.dirname(__file__), CONFIG_FILE)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False

def load_environment():
    """Load environment configuration."""
    env_path = os.path.join(os.path.dirname(__file__), ENVIRONMENT_FILE)
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading environment: {e}")
            return DEFAULT_ENVIRONMENT.copy()
    else:
        return DEFAULT_ENVIRONMENT.copy()

def save_environment(env_data):
    """Save environment configuration."""
    try:
        env_path = os.path.join(os.path.dirname(__file__), ENVIRONMENT_FILE)
        with open(env_path, 'w', encoding='utf-8') as f:
            json.dump(env_data, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving environment: {e}")
        return False

def get_db_connection():
    """Get database connection."""
    try:
        db_path = os.path.join(os.path.dirname(__file__), DB_PATH)
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def get_database_stats():
    """Get database statistics."""
    try:
        conn = get_db_connection()
        if not conn:
            return {"error": "Database connection failed"}
        
        cur = conn.cursor()
        
        # Get table info
        stats = {}
        
        # Classes table stats
        try:
            cur.execute("SELECT COUNT(*) as count FROM classes")
            stats['classes_count'] = cur.fetchone()['count']
            
            cur.execute("SELECT COUNT(DISTINCT batchID) as batches FROM classes")
            stats['batches_count'] = cur.fetchone()['batches']
            
            cur.execute("SELECT MIN(date) as min_date, MAX(date) as max_date FROM classes")
            date_range = cur.fetchone()
            stats['date_range'] = {
                'min': date_range['min_date'],
                'max': date_range['max_date']
            }
            
            # Get latest batch info
            cur.execute("SELECT MAX(batchID) as latest_batch FROM classes")
            latest_batch = cur.fetchone()['latest_batch']
            if latest_batch:
                cur.execute("SELECT COUNT(*) as count FROM classes WHERE batchID = ?", (latest_batch,))
                stats['latest_batch_count'] = cur.fetchone()['count']
                stats['latest_batch_id'] = latest_batch
            
        except sqlite3.Error:
            stats['classes_count'] = 0
            stats['batches_count'] = 0
        
        # Diff table stats
        try:
            cur.execute("SELECT COUNT(*) as count FROM diff")
            stats['diff_count'] = cur.fetchone()['count']
        except sqlite3.Error:
            stats['diff_count'] = 0
        
        conn.close()
        return stats
        
    except Exception as e:
        return {"error": str(e)}

import time
# Routes
@app.route('/')
def index():
    """Main dashboard."""
    config = load_config()
    environment = load_environment()
    db_stats = get_database_stats()
    
    return render_template('dashboard.html', 
                         config=config, 
                         environment=environment,
                         db_stats=db_stats)

@app.route('/config')
def config_page():
    """Configuration management page."""
    config = load_config()
    return render_template('config.html', config=config)

@app.route('/environment')
def environment_page():
    """Environment configuration page."""
    environment = load_environment()
    return render_template('environment.html', environment=environment)

@app.route('/database')
def database_page():
    """Database management page."""
    return render_template('database.html')

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

@app.route('/api/environment', methods=['GET'])
def get_environment():
    """Get current environment configuration."""
    environment = load_environment()
    return jsonify(environment)

@app.route('/api/environment', methods=['POST'])
def update_environment():
    """Update environment configuration."""
    try:
        new_env = request.get_json()
        
        # Save the environment configuration
        if save_environment(new_env):
            return jsonify({'success': True, 'message': 'Environment configuration saved successfully'})
        else:
            return jsonify({'error': 'Failed to save environment configuration'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Invalid environment data: {str(e)}'}), 400

@app.route('/api/database/tables')
def get_database_tables():
    """Get list of database tables."""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cur.fetchall()]
        conn.close()
        
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/database/table/<table_name>')
def get_table_data(table_name):
    """Get data from a specific table."""
    try:
        # Basic SQL injection protection
        if not table_name.replace('_', '').isalnum():
            return jsonify({'error': 'Invalid table name'}), 400
            
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cur = conn.cursor()
        
        # Get total count
        cur.execute(f"SELECT COUNT(*) as count FROM {table_name}")
        total = cur.fetchone()['count']
        
        # Get table schema
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [col['name'] for col in cur.fetchall()]
        
        # Get data with pagination
        cur.execute(f"SELECT * FROM {table_name} ORDER BY rowid DESC LIMIT ? OFFSET ?", (per_page, offset))
        rows = [dict(row) for row in cur.fetchall()]
        
        conn.close()
        
        return jsonify({
            'data': rows,
            'columns': columns,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/database/stats')
def get_database_stats_api():
    """Get database statistics."""
    stats = get_database_stats()
    return jsonify(stats)

@app.route('/api/database/query', methods=['POST'])
def execute_query():
    """Execute a custom SQL query (READ-ONLY)."""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
            
        # Basic protection - only allow SELECT statements
        if not query.upper().startswith('SELECT'):
            return jsonify({'error': 'Only SELECT queries are allowed'}), 400
            
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
            
        cur = conn.cursor()
        cur.execute(query)
        
        # Get column names
        columns = [description[0] for description in cur.description] if cur.description else []
        
        # Get results
        rows = [dict(zip(columns, row)) for row in cur.fetchall()]
        
        conn.close()
        
        return jsonify({
            'columns': columns,
            'data': rows,
            'count': len(rows)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reset/config', methods=['POST'])
def reset_config():
    """Reset configuration to defaults."""
    if save_config(DEFAULT_CONFIG.copy()):
        flash('Configuration reset to defaults successfully!', 'success')
    else:
        flash('Error resetting configuration!', 'error')
    return redirect(url_for('config_page'))

@app.route('/reset/environment', methods=['POST'])
def reset_environment():
    """Reset environment configuration to defaults."""
    if save_environment(DEFAULT_ENVIRONMENT.copy()):
        flash('Environment configuration reset to defaults successfully!', 'success')
    else:
        flash('Error resetting environment configuration!', 'error')
    return redirect(url_for('environment_page'))


# Credentials editor route
@app.route('/edit-credentials', methods=['GET', 'POST'])
def edit_credentials():
    # Read current credentials
    try:
        with open(CREDENTIALS_PATH, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except FileNotFoundError:
        creds = {
            "type": "", "project_id": "", "private_key_id": "",
            "private_key": "", "client_email": "", "client_id": "",
            "auth_uri": "", "token_uri": "",
            "auth_provider_x509_cert_url": "",
            "client_x509_cert_url": "", "universe_domain": ""
        }
    except json.JSONDecodeError:
        flash("Error: credentials.json is malformed", "danger")
        creds = {
            "type": "", "project_id": "", "private_key_id": "",
            "private_key": "", "client_email": "", "client_id": "",
            "auth_uri": "", "token_uri": "",
            "auth_provider_x509_cert_url": "",
            "client_x509_cert_url": "", "universe_domain": ""
        }

    if request.method == 'POST':
        # Extract form fields
        fields = [
            "type", "project_id", "private_key_id", "private_key",
            "client_email", "client_id", "auth_uri", "token_uri",
            "auth_provider_x509_cert_url", "client_x509_cert_url", "universe_domain"
        ]
        new_creds = {}
        for field in fields:
            val = request.form.get(field, '').strip()
            new_creds[field] = val

        # Validate non-empty for required fields
        missing = [f for f in fields if new_creds[f] == ""]
        if missing:
            flash(f"Fields missing: {', '.join(missing)}", "warning")
            return render_template('edit_credentials.html', creds=new_creds)

        # Backup old credentials
        backup_path = CREDENTIALS_PATH + '.bak.' + str(int(time.time()))
        try:
            if os.path.exists(CREDENTIALS_PATH):
                os.replace(CREDENTIALS_PATH, backup_path)
        except Exception as e:
            app.logger.warning(f"Could not backup credentials: {e}")

        # Write new credentials
        try:
            with open(CREDENTIALS_PATH, 'w', encoding='utf-8') as f:
                json.dump(new_creds, f, indent=2)
            flash("Credentials saved successfully.", "success")
            return redirect(url_for('edit_credentials'))
        except Exception as e:
            app.logger.error(f"Error writing credentials.json: {e}")
            flash("Error saving credentials.", "danger")
            return render_template('edit_credentials.html', creds=new_creds)

    # GET request
    return render_template('edit_credentials.html', creds=creds)


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    print("Starting ClassCompass Management Web GUI...")
    print("Open http://localhost:5001 in your browser")
    print("Press Ctrl+C to stop the server")
    # Run the Flask app on port 5001 to avoid conflicts
    app.run(host='0.0.0.0', port=5001, debug=True)
