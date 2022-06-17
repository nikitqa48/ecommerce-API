import datetime

def get_utc_for_midnight_in_timezone(instance):
    # print(instance)
    # local_midnight = datetime(2000, 1, 1, 0, 0, 0, tzinfo=timezone(tzstring))
    # utc = local_midnight.astimezone(timezone('UTC'))
    print(instance.filter.code)