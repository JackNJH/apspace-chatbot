#You can do `rasa run actions` in a separate terminal while using the chatbot to save time if you forgot to do that/ it randomly isnt running. 
from database.data_query import get_next_class, get_all_classes, get_all_classes_today
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

    

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
                response = f"The next class is {next_class[0]} on {next_class[1]} at {next_class[2]}."
            else:
                response = "There are no upcoming classes in the timetable."

        elif timetable_type == 'whole':
            # Logic to show the whole timetable
            all_classes = get_all_classes()

            if all_classes:
                response = "Here is the complete timetable:\n"
                for class_info in all_classes:
                    response += f"{class_info[0]} on {class_info[1]} at {class_info[2]}\n"
            else:
                response = "The timetable is currently empty."

        elif timetable_type == 'today':
            # Logic to show today's timetable
            today_classes = get_all_classes_today()

            if today_classes:
                response = "Here are today's classes:\n"
                for class_info in today_classes:
                    response += f"{class_info[0]} at {class_info[2]} in {class_info[3]}\n"
            else:
                response = "There are no classes scheduled for today."

        dispatcher.utter_message(response)
        return []
