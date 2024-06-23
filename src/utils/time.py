"""time file"""
from datetime import datetime
import pytz
from src.configs.constants import Constants


def get_current_datetime(
        time_zone: str = Constants.DEFAULT_TIME_ZONE,
        return_string: bool = True,
        is_date_only: bool = False,
        time_format: str = Constants.DEFAULT_DATETIME_FORMAT
):
    """get current datetime"""
    server_timezone = pytz.timezone(time_zone)
    if return_string is True:
        if is_date_only is False:
            return datetime.now(server_timezone).strftime(time_format)
        return datetime.now(server_timezone).strftime(Constants.DEFAULT_DATE_FORMAT)
    else:
        return datetime.now(server_timezone).replace(microsecond=0, tzinfo=None)
