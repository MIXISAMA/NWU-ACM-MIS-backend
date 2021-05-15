import pytz
from datetime import datetime

from django.conf import settings

timezone = pytz.timezone(settings.TIME_ZONE)

def to_time_zone(dt: datetime): 
    return dt.astimezone(timezone).isoformat()
