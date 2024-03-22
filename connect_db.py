import mysql.connector

def create_connection():
    try:
        conn = mysql.connector.connect(
            user='your_username',
            password='your_password',
            host='your_database_ip',
            database='your_database_name'
        )
        print("Connection established to Google Cloud MySQL Database.")
        return conn
    except mysql.connector.Error as e:
        print(e)
    return None

def close_connection(conn):
    if conn:
        conn.close()
        print("Connection to Google Cloud MySQL Database is closed.")
