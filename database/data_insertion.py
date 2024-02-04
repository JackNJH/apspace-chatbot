import sqlite3

# ADD MORE DATA OR REMOVE DATA AS YOU WISH
# YOU CAN REMOVE DATA TO CREATE FALLBACKS RESPONSES FOR THE BOT LIKE (IF ASKED FOR SEM5 RESULTS BUT THERE IS NOTHING THEN WHAT RESPONSE ETC)

def insert_sample_data():
    try:
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()
            
            # CLASSROOMS & SCHEDULES
            cursor.executemany('''
                INSERT INTO classrooms (classroom_id, class_block, class_floor)
                VALUES (?, ?, ?)
                ''', [
                    ('B-04-05', 'B', '4th Floor'),
                    ('B-04-03', 'B', '4th Floor'),
                    ('B-05-05', 'B', '5th Floor'),
                    ('B-07-09', 'B', '7th Floor'),
                    ('D-07-08', 'D', '7th Floor'),
                    ('D-07-10', 'D', '7th Floor'),
                    ('E-08-03', 'E', '8th Floor'),
                    ('Tech Lab 6-07', 'Tech Lab', '6th Floor'),
                    ('Tech Lab 5-03', 'Tech Lab', '5th Floor'),
                ])

            # I only inserted a mock schedule which means only 1 USER'S schedule. More schedules can be added here to simulate an experience for MULTIPLE user's schedules
            cursor.executemany('''
                INSERT INTO class_schedule (classroom_id, day_of_week, start_time, end_time, subject_name, class_type)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', [
                ('D-07-08', 'Monday', '08:30 AM', '10:30 AM', 'Introduction to AI', 'Tutorial'),
                ('Tech Lab 6-07', 'Monday', '10:45 AM', '12:45 PM', 'Java Programming', 'Lab'),
                ('B-04-03', 'Monday', '08:30 AM', '10:30 AM', 'Digital Security & Forensics', 'Tutorial'),
                ('E-08-03', 'Tuesday', '08:30 AM', '10:30 AM', 'Java Programming', 'Lecture'),
                ('B-07-09', 'Wednesday', '01:30 PM', '03:30 PM', 'Software Development Project', None),
                ('B-05-05', 'Thursday', '08:30 AM', '10:30 AM', 'Introduction to AI', 'Lecture'),
                ('B-04-05', 'Friday', '08:30 AM', '10:30 AM', 'Digital Security & Forensics', 'Lecture'),
            ])

            cursor.executemany('''
                INSERT INTO bus_schedule (route, start_time)
                VALUES (?, ?)
            ''', [
                ('APU to LRT', '01:00 PM'),
                ('APU to LRT', '01:30 PM'),
                ('APU to LRT', '02:00 PM'),
                ('APU to LRT', '02:30 PM'),
                ('APU to LRT', '03:00 PM'),
                ('APU to LRT', '03:30 PM'),
                ('APU to LRT', '04:00 PM'),
                ('LRT to APU', '08:00 AM'),
                ('LRT to APU', '08:30 AM'),
                ('LRT to APU', '09:00 AM'),
                ('LRT to APU', '09:30 AM'),
                ('LRT to APU', '10:00 AM'),
                ('LRT to APU', '10:30 AM'),
                ('LRT to APU', '11:00 AM'),
                ('LRT to APU', '11:30 AM'),
                ('LRT to APU', '12:00 PM'),
                ('LRT to APU', '12:30 PM'),
                ('LRT to APU', '01:00 PM'),
                ('LRT to APU', '01:30 PM'),
                ('LRT to APU', '02:00 PM'),
                ('FORTUNE PARK to APU', '10:00 AM'),
                ('FORTUNE PARK to APU', '02:00 PM'),
                ('FORTUNE PARK to APU', '09:00 PM'),
                ('APU to FORTUNE PARK', '12:00 PM'),
                ('APU to FORTUNE PARK', '04:00 PM'),
                ('APU to FORTUNE PARK', '11:00 PM'),
            ])

            # SUBJECTS
            subjects_data = [
                ('IAI', 'Introduction to AI',),
                ('DSF', 'Digital Security & Forensics',),
                ('JP', 'Java Programming',),
                ('SDP', 'Software Development Project',),
                ('NM', 'Numerical Methods',),
                ('WDT', 'Web Development',),
                ('PWP', 'Programming with Python',),
                ('DBS', 'Database Systems',),
                ('IS', 'Information Systems',),
                ('FEP', 'Fundamentals of Entrepreneurship',),
            ]

            cursor.executemany('''
                INSERT INTO subjects (subject_id, subject_name)
                VALUES (?, ?)
            ''', subjects_data)

            # RESULTS
            cursor.executemany('''
                INSERT INTO results (subject_id, semester, gpa)
                VALUES (?, ?, ?)
            ''', [
                ('IAI', 5, 3.3),
                ('DSF', 5, 3.7),
                ('JP', 5, 2.3),
                ('SDP', 5, 2.0),
                ('NM', 4, 3.0),
                ('WDT', 4, 2.7),
                ('PWP', 3, 3.0),
                ('DBS', 3, 2.3),
                ('IS', 1, 4.0),
                ('FEP', 1, 4.0),
            ])

            # APCARD (LATEST ACTIVITY)
            # theres not really a need for multiple inputs for this one because the chatbot is only catered to 1 person right now anyway....
            cursor.executemany('''
                INSERT INTO apcard (apcard_id, remaining_cash, spending_history, topup_history)
                VALUES (?, ?, ?, ?)
            ''', [
                ('TP000001', 100.0, 'Bought books', 'Added $50'),
            ])

            # FEES
            # theres not really a need for multiple inputs for this one because the chatbot is only catered to 1 person right now anyway....
            cursor.executemany('''
                INSERT INTO pending_fees (total_amount, unpaid, paid)
                VALUES (?, ?, ?)
            ''', [
                (33000.0, 24000.0, 9000.0),
            ])

            # LIBRARY STUFF
            meeting_rooms_data = [
                ('Room 1',),
                ('Room 2',),
                ('Room 3',),
            ]

            cursor.executemany('''
                INSERT INTO meeting_rooms (room_name)
                VALUES (?)
            ''', meeting_rooms_data)

            cursor.executemany('''
                INSERT INTO booked_rooms (room_id, start_time, end_time)
                VALUES (?, ?, ?)
            ''', [
                (1, '10:00 AM', '11:00 AM'),
                (2, '04:00 PM', '05:00 PM'),
            ])

    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")