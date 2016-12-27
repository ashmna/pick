import pandas

data = pandas.read_csv('../resources/menu/timestamp_Wday.csv')


data['Key'] = data['Key']

data['Key'] = data['Restaurant'].astype(str) + "-" + data['Customer'].astype(str)

data['Key'].value_counts()

# 332.0-9328       141
# 909.0-33709      125
# 71.0-33709        93
# 547.0-38973       92
# 909.0-11516       92
# 169.0-27863       86
# 495.0-23029       85
# 71.0-8747         75
# 386.0-8874        75
