from components.core.packages.lookups import QuickOptionsDateOperators,QuickOptionsDatePeriods
import datetime
import logging
import json

log = logging.getLogger("main")

year = QuickOptionsDatePeriods.get_value(QuickOptionsDatePeriods.Y)
quarter = QuickOptionsDatePeriods.get_value(QuickOptionsDatePeriods.Q)
month = QuickOptionsDatePeriods.get_value(QuickOptionsDatePeriods.M)
week = QuickOptionsDatePeriods.get_value(QuickOptionsDatePeriods.W)
day = QuickOptionsDatePeriods.get_value(QuickOptionsDatePeriods.D)

next_ = QuickOptionsDateOperators.get_value(QuickOptionsDateOperators.NEXT)
last = QuickOptionsDateOperators.get_value(QuickOptionsDateOperators.LAST)
between = QuickOptionsDateOperators.get_value(QuickOptionsDateOperators.BTWN)

quick_options_date_operator = [next_, last, between]
quick_options_date_periods = [year, quarter, month, week, day]

def decode_date_range(date_range):
    try:
        dt = json.loads(date_range)
        log.info(dt)

        start_date = ""
        end_date = ""

        date_range_extraction = 0
        operator = dt.get("operator")
        period = dt.get("period")
        value = dt.get("value")

        if (operator in quick_options_date_operator) and (period in quick_options_date_periods):
            if period == "Y":
                if int(value) <= 3 and int(value) > 0:
                    if operator == last:
                        end_date = str(datetime.datetime.now()).split(" ")[0]
                        start_date = datetime.datetime.today() - datetime.timedelta(days=int(value)*365)
                        start_date = start_date.strftime("%Y-%m-%d")
                    elif operator == next_:
                        start_date = str(datetime.datetime.now()).split(" ")[0]
                        end_date = datetime.datetime.today() + datetime.timedelta(days=int(value)*365)
                        end_date = end_date.strftime("%Y-%m-%d")

                    if len(start_date) > 0 and len(end_date) > 0:
                        date_range_extraction = 1
                    else:
                        print("No Start Date and End Date Derived for Period Y")

            elif period == "M":
                if int(value) <= 12 and int(value) > 0:
                    if operator == last:
                        end_date = str(datetime.datetime.now()).split(" ")[0]
                        start_date = datetime.datetime.today() - datetime.timedelta(days=int(value)*30)
                        start_date = start_date.strftime("%Y-%m-%d")
                    elif operator == next_:
                        start_date = str(datetime.datetime.now()).split(" ")[0]
                        end_date = datetime.datetime.today() + datetime.timedelta(days=int(value)*30)
                        end_date = end_date.strftime("%Y-%m-%d")

                        if len(start_date) > 0 and len(end_date) > 0:
                            date_range_extraction = 1
                        else:
                            print("No Start Date and End Date Derived for Period Y")

            elif period == "Q":
                if int(value) <= 4 and int(value) > 0:
                    pass

            elif period == "D":
                if int(value) <= 366 and int(value) > 0:
                    if operator == last:
                        end_date = str(datetime.datetime.now()).split(" ")[0]
                        start_date = datetime.datetime.today() - datetime.timedelta(days=int(value))
                        start_date = start_date.strftime("%Y-%m-%d")
                    elif operator == next_:
                        start_date = str(datetime.datetime.now()).split(" ")[0]
                        end_date = datetime.datetime.today() + datetime.timedelta(days=int(value))
                        end_date = end_date.strftime("%Y-%m-%d")

                    if len(start_date) > 0 and len(end_date) > 0:
                        date_range_extraction = 1
                    else:
                        print("No Start Date and End Date Derived for Period Y")

            elif period == "W":
                if int(value) <= 53 and int(value) > 0:
                    if operator == last:
                        end_date = str(datetime.datetime.now()).split(" ")[0]
                        start_date = datetime.datetime.today() - datetime.timedelta(days=int(value)*7)
                        start_date = start_date.strftime("%Y-%m-%d")
                    elif operator == next_:
                        start_date = str(datetime.datetime.now()).split(" ")[0]
                        end_date = datetime.datetime.today() + datetime.timedelta(days=int(value)*7)
                        end_date = end_date.strftime("%Y-%m-%d")

                    if len(start_date) > 0 and len(end_date) > 0:
                        date_range_extraction = 1
                    else:
                        print("No Start Date and End Date Derived for Period Y")

            if date_range_extraction == 1:
                date_range_extracted = {"start_date": start_date, "end_date": end_date}
                return date_range_extracted
            else:
                print("No Values found for start date and end date")
                date_range_extracted = {"start_date": "", "end_date": ""}
                return date_range_extracted
        else:
            date_range_extracted = {"start_date": "", "end_date": ""}
            return date_range_extracted

        # if operator == "LAST":
        #     return {"end_date": str(datetime.datetime.now()).split(" ")[0], "start_date": "2019-08-01"}
        #
        # if operator == "NEXT":
        #     return {"end_date": str(datetime.datetime.now()).split(" ")[0], "start_date": "2018-01-01"}

    except Exception as e:
        log.info("Core Engine Lib: Error in Decoding Date Range", exc_info=True)
        return False