
# Core Library for generating Calendar Datasets. Reads the core settings file for the different calendar types & parameters
# Called by IO Engine for one time loading of the calendar dataset
# System calendar users local system/server calendar settings to derive the System Calendar Dataset
# User defined Calendars like Fiscal are derived from the System Calendar


import logging
import os

log = logging.getLogger("main")

class CalendarEngine:

    _max_calendars = ""
    _calendar_types = []
    _calendar_data = []

    _system_calendar_format = ""
    _system_calendar_display_name = ""
    _system_calendar_year_start_month = ""
    _system_calendar_year_start_day = ""
    _system_calendar_year_end_month = ""
    _system_calendar_year_end_day = ""
    _system_calendar_first_day_week = ""
    _system_calendar_last_day_week = ""

    _user_defined_calendar_format = ""
    _user_defined_calendar_display_name = ""
    _user_defined_calendar_year_start_month = ""
    _user_defined_calendar_year_start_day = ""
    _user_defined_calendar_year_end_month = ""
    _user_defined_calendar_year_end_day = ""
    _user_defined_calendar_first_day_week = ""
    _user_defined_calendar_last_day_week = ""

    _max_history_period = ""
    _max_history_value = ""

    _max_forecast_period = ""
    _max_forecast_value = ""

    def __init__(self, config):
        try:
            log.info("Core Lib: Initializing Calendar generation Engine")

            self._max_calendars = config["max"]
            self._calendar_types = config["types"]
            self._system_calendar_format = config["system"].get("format")
            self._system_calendar_display_name = config["system"].get("display_name")

            system_year_start = config["system"].get("year_start")
            self._system_calendar_year_start_month = system_year_start["month"]
            self._system_calendar_year_start_day = system_year_start["day"]

            system_year_end = config["system"].get("year_end")
            self._system_calendar_year_end_month = system_year_end["month"]
            self._system_calendar_year_end_day =  system_year_end["day"]

            self._system_calendar_first_day_week = config["system"].get("first_day_week")
            self._system_calendar_last_day_week = config["system"].get("last_day_week")

            user_year_start = config["system"].get("year_start")
            self._user_calendar_year_start_month = user_year_start["month"]
            self._user_calendar_year_start_day = user_year_start["day"]

            user_year_end = config["system"].get("year_end")
            self._user_calendar_year_end_month = user_year_end["month"]
            self._user_calendar_year_end_day = user_year_end["day"]

            self._user_calendar_first_day_week = config["user_defined"].get("first_day_week")
            self._user_calendar_last_day_week = config["user_defined"].get("last_day_week")

            max_history = config["date_options"].get("_max_history_period")
            self._max_history_period = max_history["period"]
            self._max_history_value = max_history["value"]

            max_forecast = config["date_options"].get("_max_history_forecast")
            self._max_forecast_period = max_forecast["period"]
            self._max_forecast_value = max_forecast["value"]

            calendar_dataset = self.generate_calendar_dataset()

        except Exception as e:
            log.error("Core Lib: Error in initializing Calendar Engine", exc_info=True)

    def _generate_calendar_dataset(self):
        try:
            log.info("Core Lib: Generating Calendar Datasets")
            return True

        except Exception as e:
            log.error("Core Lib: Error generating Calendar Dataset ")
            return False

    def get_calendar_data(self):
        return self._calendar_data