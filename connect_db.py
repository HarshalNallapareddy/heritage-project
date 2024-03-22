import mysql.connector

def create_connection():
    try:
        print('trying to connect to Google Cloud MySQL Database')
        conn = mysql.connector.connect(
            user='root',
            password='Heritage4750',
            host='34.48.57.233',
            database='familytree'
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
