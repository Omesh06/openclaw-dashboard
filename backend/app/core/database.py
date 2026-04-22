import sqlite3
import os

DB_PATH = "openclaw_dashboard.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database tables for persistence."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # HITL Queue Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hitl_queue (
            id TEXT PRIMARY KEY,
            repo TEXT,
            branches TEXT,
            details TEXT,
            priority TEXT,
            status TEXT,
            resolution TEXT,
            created_at TEXT
        )
    ''')
    
    # Rules Engine Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS merge_rules (
            rule_name TEXT PRIMARY KEY,
            rule_value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
