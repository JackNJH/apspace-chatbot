import sqlite3

def initialize_database():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timetable (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_name TEXT,
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


def insert_sample_data():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        
        # Inserting sample data
        cursor.execute("INSERT INTO timetable (class_name, class_time, class_location) VALUES (?, ?, ?)",
                       ('Math', 'Monday 10:00 AM', 'Room 101'))
        cursor.execute("INSERT INTO timetable (class_name, class_time, class_location) VALUES (?, ?, ?)",
                       ('English', 'Tuesday 2:00 PM', 'Room 202'))
        cursor.execute("INSERT INTO timetable (class_name, class_time, class_location) VALUES (?, ?, ?)",
                       ('History', 'Wednesday 1:30 PM', 'Room 103'))
        
        # Inserting sample bus data
        cursor.execute("INSERT INTO bus_timetable (bus_time, bus_location) VALUES (?, ?)",
                       ('Monday 9:00 AM', 'APU to LRT'))
        cursor.execute("INSERT INTO bus_timetable (bus_time, bus_location) VALUES (?, ?)",
                       ('Tuesday 3:30 PM', 'APU to LRT'))
        cursor.execute("INSERT INTO bus_timetable (bus_time, bus_location) VALUES (?, ?)",
                       ('Wednesday 12:00 PM', 'LRT to APU'))

def get_next_class():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT class_name, class_time, class_location
            FROM timetable
            WHERE class_time > strftime('%Y-%m-%d %H:%M:%S', 'now')
            ORDER BY class_time
            LIMIT 1
        ''')
        next_class = cursor.fetchone()
        return next_class

def get_next_bus():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT bus_time, bus_location
            FROM bus_timetable
            WHERE bus_time > strftime('%Y-%m-%d %H:%M:%S', 'now')
            ORDER BY bus_time
            LIMIT 1
        ''')
        next_bus = cursor.fetchone()
        return next_bus

#Call function at bottom of the script and run it to clear table's data
def clear_all_data():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM timetable')
        cursor.execute('DELETE FROM bus_timetable')


initialize_database()
insert_sample_data()
