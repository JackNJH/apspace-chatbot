import sqlite3

def insert_sample_data():
    try:
        with sqlite3.connect('timetable.db') as connection:
            cursor = connection.cursor()
            
            # Inserting sample data
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('IAI Tutorial', 'Monday', '08:30 AM', 'D-07-08'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('Java Programming Lab', 'Monday', '10:45 AM', 'Tech Lab 6-07'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('Digital Security Tutorial', 'Monday', '03:45 PM', 'B-04-03'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('Java Programming Lect', 'Tuesday', '08:30 AM', 'E-08-03'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('Software Development Project', 'Wednesday', '01:30 PM', 'B-07-09'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('IAI Lect', 'Thursday', '08:30 AM', 'B-05-05'))
            cursor.execute("INSERT INTO timetable (class_name, day_of_week, class_time, class_location) VALUES (?, ?, ?, ?)",
                        ('Digital Security Lect', 'Friday', '08:30 AM', 'B-04-05'))


            
            # Inserting sample bus data
            # APU --> LRT
            days_apu_to_lrt = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            times_apu_to_lrt = ['9:00 AM', '3:30 PM']

            for day in days_apu_to_lrt:
                for time in times_apu_to_lrt:
                    cursor.execute("INSERT INTO bus_timetable (bus_time, bus_location) VALUES (?, ?)",
                                (f'{day} {time}', 'APU to LRT'))

            # LRT --> APU
            days_lrt_to_apu = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            times_lrt_to_apu = ['8:00 AM', '2:30 PM']

            for day in days_lrt_to_apu:
                for time in times_lrt_to_apu:
                    cursor.execute("INSERT INTO bus_timetable (bus_time, bus_location) VALUES (?, ?)",
                                (f'{day} {time}', 'LRT to APU'))  
    
    except sqlite3.Error as e:
        print(f"Error inserting sample data: {e}")
