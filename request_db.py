import connect_db as db
import mysql.connector

# For the users table:
def add_user(username, email, phone, password_hash):
    conn = db.create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (Username, Email, Phone, PasswordHash) VALUES (%s, %s, %s, %s)",
                       (username, email, phone, password_hash))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as e:
        print(e)
        return None



