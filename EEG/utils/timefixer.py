import time
import pytz
import datetime
import django.utils.timezone as timezone

EST = pytz.timezone('US/Eastern')
UTC = pytz.UTC
TIMEFORMAT = '%Y-%m-%d %H:%M:%S'


def str_to_timestamp(str_time):
    return time.mktime(
        datetime.datetime.strptime(str_time, TIMEFORMAT).timetuple())


def datetime_to_timestamp(struct_time):
    return time.mktime(struct_time.timetuple())


def str_to_datetime(str_time, tz=EST):
    return timezone.make_aware(
        datetime.datetime.strptime(str_time, TIMEFORMAT),
        tz).astimezone(pytz.utc)


def datetime_to_str(struct_time):
    return struct_time.strftime(TIMEFORMAT)


def make_aware(time):
    return timezone.make_aware(time,
                        timezone.get_default_timezone()).astimezone(pytz.utc)


def now():
    return timezone.make_aware(datetime.datetime.now(),
                        timezone.get_default_timezone()).astimezone(pytz.utc)


def time_overlap(in1, in2):
    a = [datetime_to_timestamp(in1[0]),
         datetime_to_timestamp(in1[1])]
    b = [datetime_to_timestamp(in2[0]),
         datetime_to_timestamp(in2[1])]
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))
