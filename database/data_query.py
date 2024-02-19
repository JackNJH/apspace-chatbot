import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

def get_bus_schedule(origin_location, destination_location):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Get next bus departure time for that route
            cursor.execute('''
                SELECT start_time FROM bus_schedule
                WHERE route = ?
            ''', (f"{origin_location} to {destination_location}",))

            schedule = cursor.fetchall()
            return schedule
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_next_class():
    try:
        current_day_of_week = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%I:%M %p')

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Get the next class for the current day
            cursor.execute('''
                SELECT subject_name, class_type, day_of_week, start_time, end_time, c.classroom_id
                FROM class_schedule cs
                INNER JOIN classrooms c ON cs.classroom_id = c.classroom_id
                WHERE day_of_week = ? AND cs.start_time >= ?
                ORDER BY start_time
                LIMIT 1
            ''', (current_day_of_week, current_time))

            next_class = cursor.fetchone()
            
        return next_class
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_all_classes():
    try:
        with sqlite3.connect('database.db') as connection:
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

        with sqlite3.connect('database.db') as connection:
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

def get_free_classrooms(day_of_week, current_time):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Calculate the minimum free time as current time + 1 hour
            end_time = (datetime.strptime(current_time, '%I:%M %p') + timedelta(hours=1)).strftime('%I:%M %p')

            # Get all classrooms that are currently unoccupied
            cursor.execute('''
                SELECT c.classroom_id, c.class_block, c.class_floor
                FROM classrooms c
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM class_schedule s
                    WHERE c.classroom_id = s.classroom_id
                    AND s.day_of_week = ?
                    AND (
                        (s.start_time >= ? AND s.start_time <= ?) OR
                        (s.end_time >= ? AND s.end_time <= ?)
                    )
                )
            ''', (day_of_week, current_time, end_time, current_time, end_time))

            free_classrooms = cursor.fetchall()
            return free_classrooms
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_apcard_details():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

        cursor.execute('''
            SELECT * FROM apcard
        ''')

        apcard_details = cursor.fetchall()
        return apcard_details
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_fees_details():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

        cursor.execute('''
            SELECT total_amount, unpaid, paid FROM pending_fees
        ''')

        fees_details = cursor.fetchall()
        return fees_details
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_cgpa():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

        cursor.execute('''
            SELECT AVG(gpa) FROM results
        ''')

        cgpa = cursor.fetchone()[0]

        return cgpa
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_results_by_semester(semester):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

        cursor.execute('''
            SELECT subject_id, gpa
            FROM results
            WHERE semester = ?
        ''', (semester,))

        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def get_meetingrooms():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

        current_time = datetime.now().strftime('%I:%M %p')
        end_time = (datetime.now() + timedelta(hours=1)).strftime('%I:%M %p')

        cursor.execute('''
            SELECT room_id
            FROM meeting_rooms
            WHERE room_id NOT IN (
                SELECT room_id
                FROM booked_rooms
                WHERE (
                    (start_time <= ? AND end_time >= ?)
                    OR (start_time <= ? AND end_time >= ?)
                    OR (start_time >= ? AND end_time <= ?)
                )
            )
            LIMIT 1
        ''', (current_time, current_time, end_time, end_time, current_time, end_time))

        meeting_rooms = cursor.fetchone()
        return meeting_rooms
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None

def insert_booking_data(room_id, start_time, end_time):
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO booked_rooms (room_id, start_time, end_time)
                VALUES (?, ?, ?)
            ''', (room_id, start_time, end_time))

            # Commit the changes
            connection.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

def delete_outdated_bookings():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Calculate the current time minus one hour
            one_hour_ago = (datetime.now() - timedelta(hours=1)).strftime('%I:%M %p')

            # Delete records older than one hour
            cursor.execute('''
                DELETE FROM booked_rooms
                WHERE end_time <= ?
            ''', (one_hour_ago,))

            # Commit the changes
            connection.commit()

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Schedule the job to run every hour
scheduler = BackgroundScheduler()
scheduler.add_job(delete_outdated_bookings, 'interval', hours=1)
scheduler.start()

# Call function to clear table's data
def clear_all_data():
    with sqlite3.connect('database.db') as connection:
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

def clear_booked_rooms_data():
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM booked_rooms')