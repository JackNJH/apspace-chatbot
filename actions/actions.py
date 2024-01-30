from database.data_query import get_next_class, get_all_classes, get_today_classes, get_bus_schedule, get_free_classrooms, get_apcard_details
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import datetime

# APCARD_DETAILS
class ActionAPCardDetails(Action):
    def name(self):
        return "action_show_apcard_details"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        apcard_details = get_apcard_details()

        if apcard_details:
            for row in apcard_details:
                apcard_id, remaining_cash, spending_history, topup_history = row
                message = f"APCard ID: {apcard_id}\nRemaining Cash: {remaining_cash}\nLatest Spending History: {spending_history}\nLatest Topup History: {topup_history}"
                dispatcher.utter_message(message)
        else:
            dispatcher.utter_message("Sorry, there was an issue fetching APCard details.")

        return []

# FREE_CLASS
class ActionFreeClassrooms(Action):
    def name(self):
        return "action_show_free_classrooms"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        day_of_week = datetime.now().strftime('%A')
        current_time = datetime.now().strftime('%I:%M %p')

        free_classrooms = get_free_classrooms(day_of_week, current_time)

        if free_classrooms:
            response = f"The available classrooms for more than an hour from now are:\n"
            response += "\n".join([f"{classroom[0]} (Block: {classroom[1]}, Floor: {classroom[2]})" for classroom in free_classrooms])
        else:
            response = f"No available classrooms on {day_of_week} at {current_time}."

        dispatcher.utter_message(response)
        return []

# BUS
class ActionBusSchedule(Action):
    def name(self):
        return "action_show_next_bus"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain):
        origin_location = tracker.get_slot("origin_location")
        destination_location = tracker.get_slot("destination_location")

        schedule = get_bus_schedule(origin_location, destination_location)

        if schedule:
            # Extract start_time values from the tuples and convert to datetime objects
            start_times = [time[0] for time in schedule]

            # Find the next closest bus time relative to the current time
            current_time = datetime.now().strftime('%I:%M %p')

            earliest_start_time = min((time for time in start_times if time >= current_time), default=None)

            # Create the response message with all start_time values
            response = f"The bus schedule from {origin_location} to {destination_location} is:\n{', '.join(start_times)}"

            if earliest_start_time:
                response += f"\n\nThe next closest bus is at {earliest_start_time}."
            else:
                response += "\n\nThere's no more buses for that route today."
        else:
            response = "No schedule found for the specified route."

        dispatcher.utter_message(response)
        return []


class ActionResetBusSlots(Action):
    def name(self):
        return "action_reset_bus_slots"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("origin_location", None), SlotSet("destination_location", None)]
    
# CLASS
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
               class_type = class_info[1] if class_info[1] is not None else ""
               response = f"Your next class is {next_class[0]} {class_type}.\nIt's on {next_class[2]} at {next_class[3]} to {next_class[4]} in {next_class[5]}."
            else:
                response = "There are no more upcoming classes today."

        elif timetable_type == 'whole':
            # Logic to show the whole timetable
            all_classes = get_all_classes()

            if all_classes:
                response = "Here is the complete timetable:\n"
                for class_info in all_classes:
                    class_type = class_info[1] if class_info[1] is not None else ""
                    response += f"{class_info[0]} {class_type} on {class_info[2]} at {class_info[3]} in {class_info[4]}\n"
            else:
                response = "The timetable is currently empty."

        elif timetable_type == 'today':
            # Logic to show today's timetable
            today_classes = get_today_classes()

            if today_classes:
                response = "Here are today's classes:\n"
                for class_info in today_classes:
                    class_type = class_info[1] if class_info[1] is not None else ""
                    response += f"{class_info[0]} {class_type} on {class_info[2]} at {class_info[3]} in {class_info[4]}\n"
            else:
                response = "There are no classes scheduled for today."

        dispatcher.utter_message(response)
        return []