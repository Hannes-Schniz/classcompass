import sqlite3
import os
import sys

SQLDIRVAR = "SQL_DIR"
DBPATHVAR = "DB_PATH"
DBPATHDEF="maps.db"
CREATECLASSESSQLFILE="createClasses.sql"
CREATEDIFFSQLFILE="createDiff.sql"

#TODO: sanitize debug output
#TODO: set correct DB_PATH when using default

def get_sql_dir():
    """Get SQL files directory from environment variable or use default."""
    sql_dir = os.environ.get(SQLDIRVAR, '').strip()
    if not sql_dir:
        sql_dir = "sql"  # Default fallback
    
    if not os.path.exists(sql_dir):
        print(f"❌ Error: SQL directory not found: {sql_dir}")
        sys.exit(1)
    
    return sql_dir

def get_db_path():
    """Get database path from environment variable or use default."""
    db_path = os.environ.get(DBPATHVAR, '').strip()
    if not db_path:
        db_path = DBPATHDEF  # Default fallback
    
    # Ensure the directory exists if it's a full path
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        print(f"📁 Creating database directory: {db_dir}")
        os.makedirs(db_dir, exist_ok=True)
    
    return db_path

def main():
    """Main function to set up the database with proper logging."""
    try:
        print("🔧 Starting database setup...")
        
        # Connect to database
        db_path = get_db_path()
        print(f"📦 Connecting to database: {db_path}")
        if os.environ.get(DBPATHVAR):
            print(f"📍 Database path set via environment variable")
        else:
            print(f"📍 Using default database path (set DB_PATH or DATABASE_PATH to override)")
        
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        print("✅ Database connection established")

        # Read SQL files
        sql_dir = get_sql_dir()
        print(f"📂 SQL files directory: {sql_dir}")
        if os.environ.get(SQLDIRVAR):
            print(f"📍 SQL directory set via environment variable")
        else:
            print(f"📍 Using default SQL directory (set SQL_DIR to override)")
        
        sql_files = [
            (os.path.join(sql_dir, CREATECLASSESSQLFILE), 'Classes table creation'),
            (os.path.join(sql_dir, CREATEDIFFSQLFILE), 'Diff table creation')
        ]
        
        for sql_file, description in sql_files:
            if not os.path.exists(sql_file):
                print(f"❌ Error: SQL file not found: {sql_file}")
                sys.exit(1)
                
            print(f"📄 Reading {description} from: {sql_file}")
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            if not sql_content.strip():
                print(f"⚠️  Warning: {sql_file} is empty")
                continue
                
            print(f"🔄 Executing {description}...")
            cur.executescript(sql_content)
            print(f"✅ {description} completed successfully")

        # Commit changes
        print("💾 Committing database changes...")
        con.commit()
        print("✅ Database changes committed successfully")
        
        # Close connection
        con.close()
        print("🔐 Database connection closed")
        print("🎉 Database setup completed successfully!")
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()