import sqlite3
from datetime import datetime

import sqlite3
from datetime import datetime

import sqlite3
from datetime import datetime

def get_next_class():
    current_day_of_week = datetime.now().strftime('%A')
    current_time = datetime.now().strftime('%I:%M %p')

    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT class_name, day_of_week, class_time, class_location
            FROM timetable
            WHERE (day_of_week = ? AND class_time > ?) OR (day_of_week > ?)
            ORDER BY class_time, day_of_week
            LIMIT 1
        ''', (current_day_of_week, current_time, current_day_of_week))

        next_class = cursor.fetchone()

    return next_class


def get_all_classes():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT class_name, day_of_week, class_time, class_location
            FROM timetable
        ''')
        all_classes = cursor.fetchall()
        return all_classes

def get_all_classes_today():
    current_day_of_week = datetime.now().strftime('%A')  # Get the current day of the week

    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            SELECT class_name, day_of_week, class_time, class_location
            FROM timetable
            WHERE day_of_week = ?
        ''', (current_day_of_week,))

        all_classes_today = cursor.fetchall()
        return all_classes_today


#Call function at bottom of the script and run it to clear table's data
def clear_all_data():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS timetable')
        cursor.execute('DROP TABLE IF EXISTS bus_timetable')
