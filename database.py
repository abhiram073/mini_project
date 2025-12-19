"""
Database module for traffic violation detection app
Handles SQLite database operations for storing violation data
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

DATABASE_PATH = 'traffic_violations.db'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create violations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            violation_type TEXT NOT NULL,
            confidence REAL NOT NULL,
            timestamp DATETIME NOT NULL,
            result_image TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create index for better performance
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_violation_type 
        ON violations(violation_type)
    ''')
    
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON violations(timestamp)
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully")

def save_violation(filename: str, violation_type: str, confidence: float, 
                  timestamp: datetime, result_image: str = '') -> int:
    """Save violation detection result to database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO violations (filename, violation_type, confidence, timestamp, result_image)
        VALUES (?, ?, ?, ?, ?)
    ''', (filename, violation_type, confidence, timestamp, result_image))
    
    violation_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return violation_id

def get_violations(filename: Optional[str] = None, limit: int = 100) -> List[Dict]:
    """Get violations from database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filename:
        cursor.execute('''
            SELECT * FROM violations 
            WHERE filename = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (filename, limit))
    else:
        cursor.execute('''
            SELECT * FROM violations 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (limit,))
    
    violations = []
    for row in cursor.fetchall():
        violations.append({
            'id': row['id'],
            'filename': row['filename'],
            'violation_type': row['violation_type'],
            'confidence': row['confidence'],
            'timestamp': row['timestamp'],
            'result_image': row['result_image']
        })
    
    conn.close()
    return violations

def get_violation_stats() -> Dict:
    """Get violation statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total violations
    cursor.execute('SELECT COUNT(*) as total FROM violations')
    total_violations = cursor.fetchone()['total']
    
    # Violations by type
    cursor.execute('''
        SELECT violation_type, COUNT(*) as count 
        FROM violations 
        GROUP BY violation_type 
        ORDER BY count DESC
    ''')
    violations_by_type = {row['violation_type']: row['count'] for row in cursor.fetchall()}
    
    # Recent violations (last 24 hours)
    cursor.execute('''
        SELECT COUNT(*) as recent 
        FROM violations 
        WHERE timestamp > datetime('now', '-1 day')
    ''')
    recent_violations = cursor.fetchone()['recent']
    
    # Average confidence
    cursor.execute('SELECT AVG(confidence) as avg_confidence FROM violations')
    avg_confidence = cursor.fetchone()['avg_confidence'] or 0
    
    conn.close()
    
    return {
        'total_violations': total_violations,
        'violations_by_type': violations_by_type,
        'recent_violations': recent_violations,
        'avg_confidence': round(avg_confidence, 2)
    }

def delete_violation(violation_id: int) -> bool:
    """Delete a violation record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM violations WHERE id = ?', (violation_id,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    
    return deleted

