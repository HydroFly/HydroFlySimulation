import matplotlib.pyplot as plt
import numpy as np


class Grapher:
    def __init__(self):
        self.data = {}
        self.time = []
        self.output = ""
        

    def record(self, name, value, t, title, only_positive=False, show_y_axis=False):
        if not self.data.get(name, None):
            self.data[name] = {'values': []}

        self.data[name]['values'].append(value)
        self.data[name]['title'] = title
        self.data[name]['only_positive'] = only_positive
        self.data[name]['show_y_axis'] = show_y_axis

        if len(self.time) < len(self.data[name]['values']):
            self.time.append(t)

        self.output += (str(round(t,4))  + ',' + title + ',' + str(value) + "\n")

    def get_data(self, name):
        if self.data.get(name, None):
            return self.data[name]['values']

    def get_latest(self, name):
        if self.data[name] is not None:
            return self.data[name]['values'][-1]

    def get_time(self):
        return self.time

    def show_plots(self):
        i = 1
        j = 1
        k = 1
        for plot in self.data:
            if k > i * j:
                if i > j:
                    j += 1
                else:
                    i += 1
            k += 1
        k = 1
        for plot in self.data:
            plt.subplot(str(j) + str(i) + str(k))
            plt.plot(self.get_time(), self.get_data(plot), '-')
            plt.plot(self.get_time(), np.full(len(self.get_time()), self.get_latest(plot)), '--')
            plt.title(self.data[plot]['title'])
            bottom, top = plt.ylim()

            if self.data[plot]['only_positive']:
                plt.ylim(0, top)
            plt.text(0, self.get_latest(plot), "{:.3f}".format(self.get_latest(plot)))

            if self.data[plot]['show_y_axis']:
                plt.axhline(0, color='red')

            k += 1
        f = open('log.txt', 'a')
        f.write(self.output)

        plt.show()
