import re
import datetime

def calcualte_min_hours_and_minutes(time_value):
    
    hours = time_value.GetHour()
    minutes = time_value.GetMinute() + 3
    if minutes >= 60:
        minutes = minutes % 60
        hours = hours + 1
    return (hours, minutes)

def is_empty(text):
    return text == ""

def are_email_addresses_valid(email_addresses):

    for current in email_addresses:
        if re.search(".+\@.+\..+", current) is None:
            return False

    return True

def convert_to_python_datetime(wx_date, wx_time):
    
    ymd = map(int, wx_date.FormatISODate().split('-'))
    hms = map(int, wx_time.FormatISOTime().split(':'))
    year, month, day = ymd
    hour, minutes, seconds = hms
    return datetime.datetime(year, month, day, hour, minutes)

def get_Wx_datetime_now(wx):
    datetime_now = datetime.datetime.now()
    now_wx_datetime = wx.DateTime()
    now_wx_datetime.Set(datetime_now.day, datetime_now.month - 1, datetime_now.year, datetime_now.hour, datetime_now.minute)
    return now_wx_datetime

def sync_date_pickup_element(wx, date_pickup):
    start_wx_datetime = get_Wx_datetime_now(wx)
    end_wx_datetime = get_Wx_datetime_now(wx)
    end_wx_datetime.SetYear(end_wx_datetime.GetYear() + 1)
    date_pickup.SetRange(start_wx_datetime, end_wx_datetime)

def sync_time_pickup_element(wx, time_pickup):
    time_now_value = get_Wx_datetime_now(wx)
    hours, minutes = calcualte_min_hours_and_minutes(time_now_value)
    time_now_value.SetHour(hours)
    time_now_value.SetMinute(minutes)
    time_now_value.SetSecond(0)
    time_pickup.SetValue(time_now_value)