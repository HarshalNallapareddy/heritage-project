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

    # Run the query
    result = run_query(connection, query)
    if result is not None:
        print("Query result:")
        for row in result:
            print(row)

    # Close the connection
    connection.close()
    print("Connection closed")

if __name__ == "__main__":
    main()
