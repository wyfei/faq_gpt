from typing import Dict, Text, Any, List, Union

from rasa_sdk import Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction


class ValidateActivityForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_activity_form"

    @staticmethod
    def activity_db() -> List[Text]:
        """Database of supported activity."""

        return [
            "星计划",
            "AIGC启航计划",
            "宝藏老师夏日企划"
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_activity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate activity value."""

        if self.is_int(value) and int(value) > 0:
            int_val = int(value)
            if int_val == 1:
                value = "星计划"
            elif int_val == 2:
                value = "AIGC启航计划"
            else:
                value = "宝藏老师夏日企划"
    
        print(value)
        if value.lower() in self.activity_db():
            # validation succeeded, set the value of the "activity" slot to value
            return {"activity": value}
        else:
            dispatcher.utter_message(response="utter_wrong_activity")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"activity": None}


class ValidateActivityTimeForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_activity_time_form"

    @staticmethod
    def activity_db() -> List[Text]:
        """Database of supported activity."""

        return [
            "星计划",
            "AIGC启航计划",
            "宝藏老师夏日企划"
        ]

    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer."""

        try:
            int(string)
            return True
        except ValueError:
            return False

    def validate_activity(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate activity value."""

        
        value = "星计划"
            
        print(value)
        if value.lower() in self.activity_db():
            # validation succeeded, set the value of the "activity" slot to value
            return {"activity": value}
        else:
            dispatcher.utter_message(response="utter_wrong_activity")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"activity": None}
        
    def validate_time(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate activity value."""

        return {"time": value}