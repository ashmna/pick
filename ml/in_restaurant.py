import pandas
from datetime import datetime, timedelta


data = pandas.read_csv("../data/orders.csv")


data['InRestaurant'] = data['TimePick'] - data['TimeArrive']

data = data[data['InRestaurant'] > 0]
data = data[data['InRestaurant'] <= 3600]

def r(time_order) :
    time_order = datetime.fromtimestamp(time_order)
    return '%s-%s-%s' % (time_order.year, time_order.month, time_order.day)

data['time'] = data['TimePick'].map(r)

print data.groupby(['time']).sum()



# "ID","Customer","Restaurant","Company","CustomerZone","RestaurantZone","TransDate","TimeStart","TimePlace","TimeFax","TimeConfirm","TimeArrive","TimePick","TimeComplete","TargetPrep","TimetoPlace","TargetDelivery","ETA","CVV2","CustomerCode","Driver","DriverShift","FlaggedDate","CustomerType","TimedOrder","VoidOperator","VoidDate","VoidTime","VoidReason","AssistedDispatch","CreatedTime","CreatedDate","Latitude","Longitude","OrderStatus","AdvancedOrder","ReasonCode","AddressID","TimeArriveDestination","wDay"
