import components.core.library.query.coreQueryOptionsDecoder as QueryDecoder
import components.core.packages.lookups as CoreLookups
import logging

# This function will decode the default date range set in the system or user preferences.
# First: Reads the metadata defined for the available operators and the periods
# Input:
#   date_range: will be a json. example {"operator":"LAST","value":"30", "period":"DYS"}

log = logging.getLogger("main")
def decode_date_range(date_range):
    try:
        log.info("Core Library: Decoding Date range")
        # Read CoreLookups.QuickOptionsDateOperators, CoreLookups.QuickOptionsDatePeriods
        # And build a logic to decode the json and return Start Date and End Date as output (json)
        if check_value(date_range):
            data_output = QueryDecoder.decode_date_range(date_range)
            log.info(data_output)
            return data_output
        else:
            pass

    except Exception as e:
        log.error("Core Library Error!! Error decoding Date range!!", exc_info=True)
        return None


def check_value(date_range):
    try:
        return True
    except Exception as e:
        return False