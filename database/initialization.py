import sqlite3

def initialize_database():
    try:
        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS timetable (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    class_name TEXT,
                    day_of_week TEXT,
                    class_time TEXT,
                    class_location TEXT
                )
            ''')


            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bus_timetable (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    bus_time TEXT,
                    bus_location TEXT
                )
            ''')
    
    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")          

