import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('ggplot')
lines = []

target_countries = ['Germany', 'France', 'Italy', 'Poland']
date_parser = lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
df = pd.read_csv('data.csv', parse_dates=['dateRep'], date_parser=date_parser, usecols=['dateRep', 'cases', 'countriesAndTerritories'])
# df = df[df.dateRep >= add_days(now(), -60)]
df = df.pivot(index='countriesAndTerritories', columns='dateRep', values='cases')
x_dates = df.columns

x_window_length = 10
fig, ax = plt.subplots(figsize=(20,5))
ax.set_xlim(x_dates[0], x_dates[x_window_length])
ax.set_ylim(0, df.max().max())
ax.set_title('COVID-19 Cases')

def init_func():
    for index, each in enumerate(target_countries):
        line, = ax.plot([], [], marker='o', label=each)
        # line.set_label(each)
        lines.append(line)
    ax.legend()


def animate_func(i):
    start_date_index = max(0, i - x_window_length)
    start_date = x_dates[start_date_index]
    end_date_index = min(i+1, len(x_dates) - 1)
    end_date = x_dates[end_date_index]
    ax.set_xlim(start_date, x_dates[max(end_date_index, x_window_length)])
    for index, each in enumerate(target_countries):
        temp_df = df.loc[each][start_date:end_date]
        x = temp_df.index.tolist()
        y = temp_df.values.tolist()
        line = lines[index]
        line.set_data(x, y)


# init_func()
# animate_func(1)

my_animation = FuncAnimation(fig=fig, func=animate_func, frames=len(x_dates), init_func=init_func, repeat=False)
plt.show()

