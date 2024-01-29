import sqlite3

def initialize_database():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            #CLASSROOMS & SCHEDULES
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classrooms (
                    classroom_id TEXT PRIMARY KEY,
                    class_block TEXT,
                    class_floor TEXT
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS class_schedule (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    classroom_id TEXT,
                    day_of_week TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    subject_name TEXT NOT NULL,
                    class_type TEXT,
                    FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id)
                )
            ''')
    
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bus_schedule (
                    bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    route TEXT NOT NULL,
                    start_time TEXT NOT NULL
                )
            ''')

            #SUBJECTS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER,
                    semester INTEGER,
                    gpa REAL,
                    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
                )
            ''')

            #APCARD (LATEST DETAILS IM ASSUMING)
            #theres not really a need for multiple inputs for this one because the chatbot is only catered to 1 person right now anyway....
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS apcard (
                    apcard_id TEXT PRIMARY KEY,
                    remaining_cash REAL,
                    spending_history TEXT,
                    topup_history TEXT
                )
            ''')

            #FEES
            #theres not really a need for multiple inputs for this one because the chatbot is only catered to 1 person right now anyway....
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pending_fees (
                    fees_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_amount REAL,
                    unpaid REAL,
                    paid REAL
                )
            ''')

            #LIBRARY STUFF
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS meeting_rooms (
                    room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_name TEXT NOT NULL
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS booked_rooms (
                    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id INTEGER,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    booking_day TEXT NOT NULL,
                    FOREIGN KEY (room_id) REFERENCES meeting_rooms(room_id)
                )
            ''')


    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")    

