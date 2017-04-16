import pandas
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

import random


def some(x, n):
    return x.ix[random.sample(x.index, n)]


data = pandas.read_csv("../data/courier-merge-data.csv")
data = data[data['km_h'] > 0]
data = data[data['km_h'] < 50]
# corr = data.corr()
#
# mask = np.zeros_like(corr, dtype=np.bool)
# mask[np.triu_indices_from(mask)] = True
#
# f, ax = plt.subplots(figsize=(11, 9))
#
# # Generate a custom diverging colormap
# cmap = sns.diverging_palette(220, 10, as_cmap=True)
#
# # Draw the heatmap with the mask and correct aspect ratio
# sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3,
#             square=True, xticklabels=5, yticklabels=5,
#             linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

week_day_0 = (data[data['week_day'] == 0]).sample(n=5000).reset_index(drop=True)
week_day_1 = (data[data['week_day'] == 1]).sample(n=5000).reset_index(drop=True)
week_day_2 = (data[data['week_day'] == 2]).sample(n=5000).reset_index(drop=True)
week_day_3 = (data[data['week_day'] == 3]).sample(n=5000).reset_index(drop=True)
week_day_4 = (data[data['week_day'] == 4]).sample(n=5000).reset_index(drop=True)
week_day_5 = (data[data['week_day'] == 5]).sample(n=5000).reset_index(drop=True)
week_day_6 = (data[data['week_day'] == 6]).sample(n=5000).reset_index(drop=True)


sns.residplot(week_day_0['time'], week_day_0['km_h'], lowess=True, color="g")
sns.residplot(week_day_1['time'], week_day_1['km_h'], lowess=True, color="r")
sns.residplot(week_day_2['time'], week_day_2['km_h'], lowess=True, color="b")
sns.residplot(week_day_3['time'], week_day_3['km_h'], lowess=True, color="c")
sns.residplot(week_day_4['time'], week_day_4['km_h'], lowess=True, color="m")
sns.residplot(week_day_5['time'], week_day_5['km_h'], lowess=True, color="g")
sns.residplot(week_day_6['time'], week_day_6['km_h'], lowess=True, color="g")


# sns.distplot(week_day_0)

# print data

# import numpy as np
# import seaborn as sns

# sns.set(style="whitegrid")
#
# time = week_day_0.time.tolist()
# km_h = week_day_0.km_h.tolist()


# Make an example dataset with y ~ x
# rs = np.random.RandomState(7)
# x = rs.normal(2, 1, 75)
# y = 2 + 1.5 * x + rs.normal(0, 2, 75)

# Plot the residuals after fitting a linear model
# sns.residplot(time, km_h, lowess=True, color="g")
#

# sns.distplot(week_day_0['km_h'])
# sns.residplot(week_day_0['time'], week_day_0['km_h'], lowess=True, color="g")
#
# sns.set(style="darkgrid")
#
# # Load the long-form example gammas dataset
# gammas = sns.load_dataset("gammas")
#
# # Plot the response with standard error
# print gammas
# sns.tsplot(data=gammas, time="timepoint", unit="subject",
#            condition="ROI", value="BOLD signal")
#
# sub_data = data.sample(n=100)
# sub_data.reset_index(drop=True)
# # print sub_data
# #
# sns.tsplot(data=sub_data, time="time", unit="week_day", condition="week_day", value="km_h")
sns.plt.show()
