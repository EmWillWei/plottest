import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import MaxNLocator
plt.style.use('ggplot')


class PlotRaceBar:
    color_index = 0
    color_mappings = {
        'United_States_of_America': '#346abd',
        'Turkey': '#fbc15e',
        'Russia': '#777777',
        'India': '#988ed5',
        'Brazil': '#8eba42',
        'United_Kingdom': '#e24a33',
        'Italy': '#ffb5b8',
        'China': '#e24a33'
    }

    def get_color(self, country):
        color = self.color_mappings.get(country)
        # 默认一个主题色只有七个颜色，超过了，需要重新分配
        if color:
            return color
        else:
            colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
            color = colors[self.color_index % len(colors)]
            self.color_mappings[country] = color
            self.color_index += 1
            return color

    def read_data(self):
        date_parser = lambda x: datetime.datetime.strptime(x, "%d/%m/%Y")
        df = pd.read_csv('data.csv', parse_dates=['dateRep'], date_parser=date_parser,
                         usecols=['dateRep', 'cases', 'countriesAndTerritories'])

        # pivot 一下 方面我们接下来取数据
        pivot_df = df.pivot(index='dateRep', columns='countriesAndTerritories', values='cases')
        pivot_df = pivot_df.fillna(0)
        pivot_df = pivot_df.astype(np.int32)
        return pivot_df

    def plot(self):
        df = self.read_data()
        x_dates = df.index
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.set_title('COVID-19 Cases')
        ax.xaxis.set_ticks_position('top')

        def format_number(x, pos):
            'The two args are the value and tick position'
            if x >= 1000000:
                return '{:1.1f}M'.format(x * 1e-6)
            elif x >= 1000:
                return '{:1.0f}K'.format(x * 1e-3)
            else:
                return int(x)

        def animate_func(i):
            ax.clear()
            ax.set_xlim(0, df.max().max() * 1.1)
            temp_data = df.iloc[i].sort_values(ascending=False).head(20).sort_values() # temp_data 是一个pd.Series
            # temp_data = temp_data[temp_data > 0]  # 过滤掉数量为0的
            colors = []
            for country in temp_data.index:
                color = self.get_color(country)
                colors.append(color)

            ax.barh(temp_data.index, temp_data.values, height=0.8, color=colors)

            index = -1
            for country, value in temp_data.items():
                index += 1
                # ax.barh(country, value)
                if value > 0:
                    ax.text(value, index, value)
            ax.text(0.8, 0.3, x_dates[i].date(), transform=ax.transAxes, fontsize=16)
            formatter = FuncFormatter(format_number)
            ax.xaxis.set_major_formatter(formatter)
            ax.grid(axis='y')

        # animate_func(0)  # 测试用的 只画某一天的图
        my_animation = FuncAnimation(fig=fig, func=animate_func, frames=len(x_dates), repeat=False, interval=500)
        # my_animation.save('covid_race_bar.mp4', fps=5)
        plt.show()


if __name__ == '__main__':
    t = PlotRaceBar()
    t.plot()