import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Util.DateTimeHelper import add_days, now

plt.style.use('ggplot')
bars = []

target_countries = ['Germany', 'France', 'Italy', 'Poland']
date_parser = lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
df = pd.read_csv('data.csv', parse_dates=['dateRep'], date_parser=date_parser, usecols=['dateRep', 'cases', 'countriesAndTerritories'])
df = df[df.dateRep >= add_days(now(), -60)]

df = df.pivot(index='dateRep', columns='countriesAndTerritories', values='cases')
x_dates = df.index

x_window_length = 10
fig, ax = plt.subplots(figsize=(20,5))
ax.set_title('COVID-19 Cases')
ax.xaxis.set_ticks_position('top')


# def init_func():
#     for index, each in enumerate(target_countries):
#         bar = ax.barh(index, 0, tick_label=each)
#         # line.set_label(each)
#         bars.append(bar)
#     ax.legend()

def animate_func(i):
    ax.clear()
    temp_df = df.iloc[i].sort_values(ascending=False).head(10).sort_values()
    # ax.barh(temp_df.index, temp_df.values)
    index = -1
    for country, value in temp_df.items():
        index += 1
        ax.barh(country, value)
        ax.text(value, index, value)
    ax.text(0.8, 0.3, x_dates[i].date(), transform=ax.transAxes, fontsize=16)
    ax.grid(axis='y')
    plt.box(False)

# init_func()
# animate_func(1)

my_animation = FuncAnimation(fig=fig, func=animate_func, frames=len(x_dates), repeat=False)
plt.show()
