import pyodbc

def run_query(query):
    # Define the connection string
    cnxn_str = (
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=tcp:berrydiscoserverl.database.windows.net,1433;'  # Replace with your server
        'DATABASE=BerryDiscoDatabase;'                             # Replace with your database
        'UID=sqladmin;'                                            # Replace with your username
        'PWD={girlhacks24!};'                                      # Replace with your password
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30;'
    )

    try:
        # Establish the connection
        conn = pyodbc.connect(cnxn_str)
        cursor = conn.cursor()
        
        # Execute the SQL query
        cursor.execute(query)
        conn.commit()  # Ensure transaction is committed for non-SELECT queries

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        # Check if defined before closing
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

# Define the SQL query to create the table
create_table_query = """
CREATE TABLE Swapnil (
    ID INT PRIMARY KEY IDENTITY(1,1),
    Title NVARCHAR(100),
    Artist NVARCHAR(100),
    Album NVARCHAR(100),
    ReleaseYear INT
);
"""

# Run the query to create the table
run_query(create_table_query)
print("Table 'Songs' created successfully.")