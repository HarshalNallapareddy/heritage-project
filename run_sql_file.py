import mysql.connector
from connect_db import create_connection, close_connection


def run_sql_file(filename):
  """
  Executes SQL commands from a file sequentially, printing any errors.
  """
  try:
    with open(filename, 'r') as f:
      connection = create_connection()
      if connection is None:
        return

      cursor = connection.cursor()
      for line in f:
        # Skip comments and empty lines
        if not line.strip() or line.startswith('--'):
          continue
        try:
          # Execute the SQL statement
          cursor.execute(line.strip())

          # Fetch and consume the results (if any)
          if cursor.with_rows:
            result = cursor.fetchall()
            # Process or print the results if needed

          # Close the cursor before COMMIT (or other commands)
          cursor.close()

          connection.commit()  # Commit changes after each statement
          print(f"Executed: {line.strip()}")
        except mysql.connector.Error as err:
          print(f"Error on line '{line.strip()}': {err}")
          # Close the cursor in case of errors
          cursor.close()

      connection.close()
      print("Connection closed")
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")


if __name__ == "__main__":
  # Get filename from user input (replace with argument parsing if needed)
  filename = input("Enter the SQL file name: ")
  run_sql_file(filename)
