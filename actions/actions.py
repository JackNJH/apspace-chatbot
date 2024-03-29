from database.data_query import get_next_class, get_all_classes, get_today_classes, get_bus_schedule, get_free_classrooms, get_apcard_details, get_fees_details, get_cgpa, get_results_by_semester, get_meetingrooms, insert_booking_data
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime, timedelta
import requests, random

# BUS
class ActionBusSchedule(Action):
    def name(self):
        return "action_show_next_bus"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        origin_location = tracker.get_slot("origin_location")
        destination_location = tracker.get_slot("destination_location")

        schedule = get_bus_schedule(origin_location, destination_location)

        if schedule:
            start_times = [time[0] for time in schedule]
            start_times_formatted = []

            # Convert time format
            for time_str in start_times:
                time_obj = datetime.strptime(time_str, "%H:%M")
                time_str_12hr = time_obj.strftime("%I:%M %p")  
                start_times_formatted.append(time_str_12hr)

            # Find the next closest bus time relative to the current time
            current_time = datetime.now().strftime('%H:%M')

            earliest_start_time = min((time for time in start_times if time >= current_time), default=None)

            # Create the response message with all start_time values
            response = f"The bus schedule from {origin_location} to {destination_location} is:  \n{', '.join(start_times_formatted)}"

            if earliest_start_time:
                earliest_start_time_12hr = datetime.strptime(earliest_start_time, "%H:%M").strftime("%I:%M %p")
                response += f"\n\nThe next closest bus is at {earliest_start_time_12hr}."
            else:
                response += "\n\nThere's no more buses for that route today."
        else:
            response = "No schedule found for the specified route."

        dispatcher.utter_message(response)
        return [SlotSet("origin_location", None), SlotSet("destination_location", None)]

    
# CLASS
class ActionShowTimetable(Action):
    def name(self):
        return 'action_show_class_timetable'

    def convert_to_12_hour_format(self, time_str):
        time_obj = datetime.strptime(time_str, '%H:%M')
        return time_obj.strftime('%I:%M %p')

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        timetable_type = tracker.get_slot('class_timetable_type')
        response = ""

        if timetable_type == 'next':
            # Logic to show next class
            next_class = get_next_class()

            if next_class:
               class_type = next_class[1] if next_class[1] is not None else ""
               start_time_12h = self.convert_to_12_hour_format(next_class[3])
               end_time_12h = self.convert_to_12_hour_format(next_class[4])
               response = f"Your next class is {next_class[0]} {class_type}.  \nIt's on {next_class[2]} at {start_time_12h} to {end_time_12h} in {next_class[5]}."
            else:
                response = "There are no more upcoming classes today."

        elif timetable_type == 'whole':
            # Logic to show the whole timetable
            all_classes = get_all_classes()

            if all_classes:
                response = "Here is the complete timetable:  \n"
                for class_info in all_classes:
                    class_type = class_info[1] if class_info[1] is not None else ""
                    start_time_12h = self.convert_to_12_hour_format(class_info[3])
                    end_time_12h = self.convert_to_12_hour_format(class_info[4])
                    response += f"{class_info[0]} {class_type} on {class_info[2]} at {start_time_12h} to {end_time_12h} in {class_info[5]}  \n"
            else:
                response = "The timetable is currently empty."

        elif timetable_type == 'today':
            # Logic to show today's timetable
            today_classes = get_today_classes()

            if today_classes:
                response = "Here are today's classes:  \n\n"
                for class_info in today_classes:
                    class_type = class_info[1] if class_info[1] is not None else ""
                    start_time_12h = self.convert_to_12_hour_format(class_info[3])
                    end_time_12h = self.convert_to_12_hour_format(class_info[4])
                    response += f"{class_info[0]} {class_type} from {start_time_12h} to {end_time_12h} in {class_info[5]}. \n"
            else:
                response = "There are no classes scheduled for today."

        dispatcher.utter_message(response)
        return []
    

# FREE_CLASS
class ActionFreeClassrooms(Action):
    def name(self):
        return "action_show_free_classrooms"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        day_of_week = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%I:%M %p')
        end_time = (datetime.now() + timedelta(hours=2)).strftime('%I:%M %p')

        free_classrooms = get_free_classrooms()

        if free_classrooms:
            response = f"The available classrooms from {current_time} to {end_time} are:  \n"
            response += "  \n".join([f"{classroom[0]} (Block: {classroom[1]}, Floor: {classroom[2]})" for classroom in free_classrooms])
        else:
            response = f"No available classrooms on {day_of_week} at {current_time}."

        dispatcher.utter_message(response)
        return []


# APCARD_DETAILS
class ActionAPCardDetails(Action):
    def name(self):
        return "action_show_apcard_details"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        apcard_details = get_apcard_details()

        if apcard_details:
            for row in apcard_details:
                apcard_id, remaining_cash, spending_history, topup_history = row
                message = f"APCard ID: {apcard_id}  \nRemaining Cash: {remaining_cash}  \nLatest Spending History: {spending_history}  \nLatest Topup History: {topup_history}"
                dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("Sorry, there was an issue fetching APCard details.")

        return []
    

# FEES
class ActionPendingFees(Action):
    def name(self):
        return "action_show_pending_fees"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        fees_details = get_fees_details()

        if fees_details:
            for row in fees_details:
                total_amount, unpaid, paid = row
                message = f"Total Course Fees: {total_amount}  \nOutstanding Amount: {unpaid}  \nPaid: {paid}"
                dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("Sorry, there was an issue fetching fee details.")

        return []

# SUBJECT RESULTS
class ActionUtterCGPA(Action):
    def name(self) -> Text:
        return "action_show_cgpa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cgpa = get_cgpa()

        if cgpa: 
            dispatcher.utter_message(text=f"Your Cumulative GPA (CGPA) is: {cgpa:.2f}")
        else:
            dispatcher.utter_message(text="Sorry, there was an issue fetching result details.")

        return []


class ActionShowSemesterResults(Action):
    def name(self):
        return 'action_show_semester_results'

    def run(self, dispatcher, tracker, domain):
        semester = tracker.get_slot('semester')

        if semester:
            results = get_results_by_semester(semester)
            
            if results:
                message = f"Results for semester {semester}:  \n"
                for subject_id, gpa in results:
                    message += f"{subject_id}: {gpa}GPA  \n"
            else:
                message = f"No results available for semester {semester}."

            dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("I'm sorry, I couldn't understand the semester number.")

        return [SlotSet('semester', None)] 


class ActionBookRoom(Action):
    def name(self) -> Text:
        return 'action_book_room'
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        meeting_rooms = get_meetingrooms()

        if meeting_rooms:
            user_selected_room_id = meeting_rooms[0]
            current_time = datetime.now().strftime('%H:%M')
            end_time = (datetime.now() + timedelta(hours=1)).strftime('%H:%M')

            # Insert booking data
            insert_booking_data(user_selected_room_id, current_time, end_time)

            current_time_12hr = datetime.now().strftime('%I:%M %p') 
            end_time_12hr = (datetime.now() + timedelta(hours=1)).strftime('%I:%M %p')

            dispatcher.utter_message(f"Room {user_selected_room_id} booked from {current_time_12hr} to {end_time_12hr}")
        else:
            dispatcher.utter_message("No available rooms for booking at the moment.")

        return []
    

class ActionGetCurrentTime(Action):
    def name(self) -> Text:
        return "action_get_current_time"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.now().strftime("%I:%M %p")
        
        responses = [
            f"The current time is {current_time}.",
            f"It's currently {current_time}.",
            f"The time is {current_time}.",
            f"The current time is {current_time}.",
            f"The time is currently {current_time}.",
            f"It is {current_time} right now."
        ]

        random.shuffle(responses)

        dispatcher.utter_message(text=responses[0])

        return []


class ActionGetWeatherForecast(Action):
    def name(self) -> Text:
        return "action_get_weather_forecast"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        location = "Kuala Lumpur" 
        
        # Make request to the weather API
        api_key = "3d76ffa4ffbc075bd90dcae88a4e3c25"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        
        responses = []
        
        if response.status_code == 200:
            data = response.json()
            weather_description = data['weather'][0]['description']
            temperature_kelvin = data['main']['temp']
            temperature_celsius = round(temperature_kelvin - 273.15, 2)

            responses.append(f"The current weather state in {location} is {weather_description} with a temperature of {temperature_celsius}°C.")
            responses.append(f"The weather shows a {weather_description} in {location} right now, with a temperature of {temperature_celsius}°C.")
            responses.append(f"{location} has {weather_description} with a temperature of {temperature_celsius}°C at the moment.")
            
            random.shuffle(responses)
            
            dispatcher.utter_message(text=responses[0])
        else:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the weather forecast at the moment. Please try again later.")
        
        return []


