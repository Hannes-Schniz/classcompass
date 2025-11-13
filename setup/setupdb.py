import sqlite3
import os
import sys
from constants import dbParams, logLevel


DEFSQLPATH = "setup/sql"
SQLDIRVAR = "SQL_DIR"
DBPATHVAR = "DB_PATH"
DBPATHDEF="maps.db"

#TODO: sanitize debug output
#TODO: set correct DB_PATH when using default

def get_sql_dir():
    """Get SQL files directory from environment variable or use default."""
    sql_dir = os.environ.get(dbParams.SQLDIRVAR.value, '').strip()
    if not sql_dir:
        sql_dir = DEFSQLPATH  # Default fallback
    
    if not os.path.exists(sql_dir):
        print(f"[{logLevel.ERROR.value}] SQL directory not found: {sql_dir}")
        sys.exit(1)
    
    return sql_dir

def get_db_path():
    """Get database path from environment variable or use default."""
    db_path = os.environ.get(dbParams.DBPATHVAR.value, '').strip()
    if not db_path:
        db_path = dbParams.DBPATHDEF.value  # Default fallback
    # Ensure the directory exists if it's a full path
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        print(f"[{logLevel.INFO.value}] Creating database directory: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    return db_path

def main():
    """Main function to set up the database with proper logging."""
    try:
        print(f"[{logLevel.INFO.value}] Starting database setup...")
        
        # Connect to database
        db_path = get_db_path()
        print(f"[{logLevel.INFO.value}] Connecting to database: {db_path}")
        if os.environ.get(dbParams.DBPATHVAR.value):
            print(f"[{logLevel.INFO.value}] Database path set via environment variable")
        else:
            print(f"[{logLevel.INFO.value}] Using default database path (set DB_PATH or DATABASE_PATH to override)")
        
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        print(f"[{logLevel.INFO.value}] Database connection established")

        # Read SQL files
        sql_dir = get_sql_dir()
        print(f"[{logLevel.INFO.value}] SQL files directory: {sql_dir}")
        if os.environ.get(dbParams.SQLDIRVAR.value):
            print(f"[{logLevel.INFO.value}] SQL directory set via environment variable")
        else:
            print(f"[{logLevel.INFO.value}] Using default SQL directory (set SQL_DIR to override)")
        
        sql_files = [
            (os.path.join(sql_dir, dbParams.CREATECLASSESSQLFILE.value), 'Classes table creation'),
            (os.path.join(sql_dir, dbParams.CREATEDIFFSQLFILE.value), 'Diff table creation')
            (os.path.join(sql_dir, dbParams.CREATENOTIFICATIONFILE.value)), 'Notification table creation')
        ]
        
        for sql_file, description in sql_files:
            if not os.path.exists(sql_file):
                print(f"[{logLevel.ERROR.value}] Error: SQL file not found: {sql_file}")
                sys.exit(1)
                
            print(f"[{logLevel.INFO.value}] Reading {description} from: {sql_file}")
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            if not sql_content.strip():
                print(f"[{logLevel.WARNING.value}]  Warning: {sql_file} is empty")
                continue
                
            print(f"[{logLevel.INFO.value}] Executing {description}...")
            cur.executescript(sql_content)
            print(f"[{logLevel.INFO.value}] {description} completed successfully")

        # Commit changes
        print(f"[{logLevel.INFO.value}] Committing database changes...")
        con.commit()
        print(f"[{logLevel.INFO.value}] Database changes committed successfully")
        
        # Close connection
        con.close()
        print(f"[{logLevel.INFO.value}] Database connection closed")
        print(f"[{logLevel.INFO.value}] Database setup completed successfully!")
        
    except sqlite3.Error as e:
        print(f"[{logLevel.ERROR.value}] Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"[{logLevel.ERROR.value}] File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[{logLevel.ERROR.value}] Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
