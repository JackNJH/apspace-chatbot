# File for testing database retrieval
import sqlite3
from initialization import initialize_database
from data_insertion import insert_sample_data
from data_query import get_next_class, get_all_classes, clear_all_data, get_today_classes, get_bus_schedule, clear_booked_rooms_data

# initialize_database()
# insert_sample_data()

def show_all_tables_and_data():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Get the list of tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            # Iterate over each table and fetch all rows
            for table in tables:
                table_name = table[0]
                print(f"\nTable: {table_name}\n")

                # Fetch all rows from the current table
                cursor.execute(f"SELECT * FROM {table_name};")
                rows = cursor.fetchall()

                # Display the column names
                column_names = [description[0] for description in cursor.description]
                print(" | ".join(column_names))

                # Display the data
                for row in rows:
                    print(" | ".join(map(str, row)))
    except sqlite3.Error as e:
        print(f"Error showing tables and data: {e}")





# show_all_tables_and_data()
# clear_all_data()
# clear_booked_rooms_data()