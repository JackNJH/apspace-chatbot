from database.data_query import get_next_class, get_all_classes, get_today_classes, get_bus_schedule
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

#BUS
class ActionBusSchedule(Action):
    def name(self):
        return "action_show_next_bus"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        origin_location = tracker.get_slot("origin_location")
        destination_location = tracker.get_slot("destination_location")

        schedule = get_bus_schedule(origin_location, destination_location)

        if schedule:
            # Extract start_time values from the tuples and convert to datetime objects
            start_times = [datetime.strptime(time[0], '%I:%M %p') for time in schedule]

            # Find the next closest bus time relative to the current time
            current_time = datetime.now()
            next_closest_time = next((time for time in start_times if time > current_time), None)

            # Create the response message with all start_time values
            formatted_start_times = [time.strftime('%I:%M %p') for time in start_times]
            response = f"The bus schedule from {origin_location} to {destination_location} is:\n{', '.join(formatted_start_times)}"

            if next_closest_time:
                next_closest_time_str = next_closest_time.strftime('%I:%M %p')
                response += f"\n\nThe next closest bus is at {next_closest_time_str}."
        else:
            response = "No schedule found for the specified route."

        dispatcher.utter_message(response)
        return []


class ActionResetBusSlots(Action):
    def name(self):
        return "action_reset_bus_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("origin_location", None), SlotSet("destination_location", None)]
    
#CLASS
class ActionShowTimetable(Action):
    def name(self):
        return 'action_show_class_timetable'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        timetable_type = tracker.get_slot('class_timetable_type')
        response = ""

        if timetable_type == 'next':
            # Logic to show next class
            next_class = get_next_class()

            if next_class:
               response = f"Your next class is {next_class[0]} {next_class[1]}.\nIt's on {next_class[2]} at {next_class[3]} to {next_class[4]} in {next_class[5]}."
            else:
                response = "There are no upcoming classes in the timetable."

        elif timetable_type == 'whole':
            # Logic to show the whole timetable
            all_classes = get_all_classes()

            if all_classes:
                response = "Here is the complete timetable:\n"
                for class_info in all_classes:
                    response += f"{class_info[0]} {class_info[1]} on {class_info[2]} at {class_info[3]} in {class_info[4]}\n"
            else:
                response = "The timetable is currently empty."

        elif timetable_type == 'today':
            # Logic to show today's timetable
            today_classes = get_today_classes()

            if today_classes:
                response = "Here are today's classes:\n"
                for class_info in today_classes:
                    response += f"{class_info[0]} {class_info[1]} on {class_info[2]} at {class_info[3]} in {class_info[4]}\n"
            else:
                response = "There are no classes scheduled for today."

        dispatcher.utter_message(response)
        return []