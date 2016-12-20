import time
import datetime
import pandas


def to_date_time(str):
    if isinstance(str, basestring):
        return time.mktime(datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S").timetuple())
    return 0


data = pandas.read_csv('../resources/menu/random_data.csv')

# replace -([0-9])- -0$1-
# replace -([0-9])\s -0$1
# replace 1900 2000

data['TransDate'] = data['TransDate'].map(to_date_time)
data['TimeStart'] = data['TimeStart'].map(to_date_time)
data['TimeFax'] = data['TimeFax'].map(to_date_time)
data['TimeConfirm'] = data['TimeConfirm'].map(to_date_time)
data['TimeArrive'] = data['TimeArrive'].map(to_date_time)
data['TimePick'] = data['TimePick'].map(to_date_time)
data['TimeComplete'] = data['TimeComplete'].map(to_date_time)
data['TargetPrep'] = data['TargetPrep'].map(to_date_time)
data['TimetoPlace'] = data['TimetoPlace'].map(to_date_time)
data['TargetDelivery'] = data['TargetDelivery'].map(to_date_time)

#
data['InRestaurant'] = data['TimePick'] - data['TimeArrive'];

head = data.head()

r = 5
