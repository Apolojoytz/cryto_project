# voting_system/database/db_connection.py
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL/MariaDB: {e}")
        return None

def execute_query(query, params=None, fetch=False, fetch_one=False, lastrowid=False):
    """Execute SQL query"""
    connection = get_db_connection()
    if not connection:
        return None
    
    cursor = None
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        elif fetch_one:
            result = cursor.fetchone()
        elif lastrowid:
            connection.commit()
            result = cursor.lastrowid
        else:
            connection.commit()
            result = cursor.rowcount
        
        return result
    except Error as e:
        print(f"❌ Database error: {e}")
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()