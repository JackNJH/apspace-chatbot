import sqlite3
from datetime import datetime

def get_next_class():
    try:
        current_day_of_week = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%I:%M %p')

        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT subject_name, day_of_week, start_time, end_time, c.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                WHERE (day_of_week = ? AND start_time > ?) OR (day_of_week > ?)
                ORDER BY start_time, day_of_week
                LIMIT 1
            ''', (current_day_of_week, current_time, current_day_of_week))

            next_class = cursor.fetchone()

        return next_class
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_all_classes():
    try:
        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT cs.subject_name, cs.day_of_week, 
                       cs.start_time, cs.end_time,
                       cs.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
            ''')
            all_classes = cursor.fetchall()
            return all_classes
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_today_classes():
    try:
        current_day_of_week = datetime.now().strftime('%A')

        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT cs.subject_name, cs.day_of_week, cs.start_time, cs.end_time, cs.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                WHERE cs.day_of_week = ?
            ''', (current_day_of_week,))

            all_classes_today = cursor.fetchall()
            return all_classes_today
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None



#Call function at bottom of the script and run it to clear table's data
def clear_all_data():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS classrooms')
        cursor.execute('DROP TABLE IF EXISTS class_schedule')
        cursor.execute('DROP TABLE IF EXISTS bus_schedule')
        cursor.execute('DROP TABLE IF EXISTS subjects')
