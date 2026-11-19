from datetime import datetime
from zoneinfo import ZoneInfo


def get_city_time(city_timezone: str) -> str:
    """Get the current local time for a city."""

    current_time = datetime.now(ZoneInfo(city_timezone))

    return current_time.strftime("%d-%m-%Y %I:%M %p")