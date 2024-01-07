#You can do `rasa run actions` in a separate terminal while using the chatbot to save time if you forgot to do that/ it randomly isnt running. 
from database import initialize_database, get_next_class, get_next_bus
from typing import Dict, Any, Text, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionNextTimetable(Action):
    def name(self):
        return 'action_next_timetable'

    def run(self, dispatcher, tracker, domain):
        timetable_type = tracker.get_slot('timetable_type')

        if timetable_type == 'class':
            next_class = get_next_class()
            if next_class:
                dispatcher.utter_message("Your next class is {} at {} in {}".format(next_class[0], next_class[1], next_class[2]))
            else:
                dispatcher.utter_message("No upcoming classes found.")
        elif timetable_type == 'bus':
            next_bus = get_next_bus()
            if next_bus:
                dispatcher.utter_message("The next bus is scheduled for {} from {}".format(next_bus[0], next_bus[1]))
            else:
                dispatcher.utter_message("No upcoming buses found.")
        else:
            dispatcher.utter_message("I'm sorry, I couldn't understand the timetable type.")

        return []