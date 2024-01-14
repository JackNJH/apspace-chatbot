import sqlite3
from datetime import datetime, timedelta

def get_next_class():
    try:
        current_day_of_week = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%I:%M %p')

        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()

            # Get the next class for the current day
            cursor.execute('''
                SELECT subject_name, class_type, day_of_week, start_time, end_time, c.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                WHERE day_of_week = ? AND start_time >= ?
                ORDER BY start_time
                LIMIT 1
            ''', (current_day_of_week, current_time))

            next_class = cursor.fetchone()

            # If no more classes for the current day, find the earliest class for the next available day
            if not next_class:
                next_day = (datetime.now() + timedelta(days=1)).strftime('%A')

                # Loop until a day with classes is found
                while not next_class:
                    cursor.execute('''
                        SELECT subject_name, class_type, day_of_week, start_time, end_time, c.classroom_id
                        FROM class_schedule cs
                        INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                        WHERE day_of_week = ?
                        ORDER BY start_time
                        LIMIT 1
                    ''', (next_day,))
                    next_class = cursor.fetchone()

                    # Move to the next day
                    next_day = (datetime.strptime(next_day, '%A') + timedelta(days=1)).strftime('%A')

        return next_class
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_all_classes():
    try:
        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT cs.subject_name, cs.class_type, cs.day_of_week, cs.start_time, cs.classroom_id
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
                SELECT cs.subject_name, cs.class_type, cs.day_of_week, cs.start_time, cs.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                WHERE cs.day_of_week = ?
            ''', (current_day_of_week,))

            all_classes_today = cursor.fetchall()
            return all_classes_today
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None


#Call function to clear table's data
def clear_all_data():
    with sqlite3.connect('timetable.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DROP TABLE IF EXISTS classrooms')
        cursor.execute('DROP TABLE IF EXISTS class_schedule')
        cursor.execute('DROP TABLE IF EXISTS bus_schedule')
        cursor.execute('DROP TABLE IF EXISTS subjects')
        cursor.execute('DROP TABLE IF EXISTS results')
        cursor.execute('DROP TABLE IF EXISTS apcard')
        cursor.execute('DROP TABLE IF EXISTS pending_fees')
        cursor.execute('DROP TABLE IF EXISTS attendance')
        cursor.execute('DROP TABLE IF EXISTS meeting_rooms')
        cursor.execute('DROP TABLE IF EXISTS booked_rooms')
        cursor.execute('DROP TABLE IF EXISTS borrowed_books')