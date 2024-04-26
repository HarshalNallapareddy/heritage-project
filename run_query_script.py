import mysql.connector
from connect_db import create_connection, close_connection


query = "SELECT COUNT(*) from AccessLogs"


def run_query(connection, query):
    try:
        cursor = connection.cursor()

        # Execute the query
        cursor.execute(query)

        # Fetch all the rows
        result = cursor.fetchall()

        return result

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def main():
    # Connect to the database
    connection = create_connection()
    if connection is None:
        return

    # Example query
    username = 'frederick'
    cursor = connection.cursor()
    print("Connection established")
    # Run the query
    cursor.execute("SELECT UserID FROM Users WHERE Username = %s",
                    (username,))
    userid = cursor.fetchone()[0] #tuple object
    cursor.fetchall()
    print("got userid: " + str(userid))
    cursor.execute("SELECT TreeID FROM TreeAccess WHERE UserID = %s",
                    (userid,))
    print(cursor.fetchone()[0])

    # Close the connection
    connection.close()
    print("Connection closed")

if __name__ == "__main__":
    main()
