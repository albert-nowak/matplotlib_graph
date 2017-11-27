import csv
import os

from collections import OrderedDict

import matplotlib.pyplot as plt

from numpy import mean


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_PATH, 'data')


class Graph:
    """
    Graph class to handle drawing 5 star graph
    in `communication human-computer` lab at PUT.
    """

    FILENAMES_MAPPING = OrderedDict([
        ('rsel.csv', '1-Evol-RS'),
        ('cel-rs.csv', '1-Coev-RS'),
        ('2cel-rs.csv', '2-Coev-RS'),
        ('cel.csv', '1-Coev'),
        ('2cel.csv', '2-Coev'),
    ])

    MARKERS = ['o', '^', 's', 'd', 'D']

    def _get_data_for_left_plot(self, filename):
        """
        Returns data for the left plot.

        On the X-axe are values from the first column,
        on the Y-axe there is a mean of all the remaining columns.

        :param filename: filename to read data from.
        :return: return dictionary with x_axe and y_axe data.
        """
        result = {
            'x_data': [],
            'y_data': [],
        }
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)  # skip headers
            for line in reader:
                result['x_data'].append(float(line[1]) / 1000)
                result['y_data'].append(
                    mean([float(num) for num in line[2:]]) * 100)
        return result

    def _get_data_for_box_plot(self, filename):
        """Returns data for the box plot."""
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            result = [line for line in reader][-1][2:]
            return [float(data) * 100 for data in result]

    def run(self):
        """Main method."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 7))
        ax1_1 = ax1.twiny()

        boxes = []  # boxes for a boxplot
        for i, (filename, display_name) in enumerate(self.FILENAMES_MAPPING.items()):
            full_path = os.path.join(DATA_PATH, filename)
            boxes.append(self._get_data_for_box_plot(full_path))
            data = self._get_data_for_left_plot(full_path)
            ax1.plot(
                data['x_data'],
                data['y_data'],
                label=display_name,
                marker=self.MARKERS[i],
                markevery=20,
                markeredgecolor='black',
                markeredgewidth=.5
            )

        # left plot
        ax1.grid(color='k', linewidth=.5, linestyle=':')
        ax1.set_xlabel('Rozegranych gier (x1000)')
        ax1.set_ylabel('Odsetek wygranych gier [%]')
        ax1_1.set_xlabel('Pokolenie')
        ax1.set_xlim(0, 500)
        ax1.set_ylim(60, 100)
        ax1_1.set_xlim(200, 0)
        handles, labels = ax1.get_legend_handles_labels()
        ax1.legend(handles, labels)

        # right plot
        meanpointprops = dict(marker='o', markeredgecolor='b', markerfacecolor='b')
        with plt.style.context('classic'):
            labels = [v for k, v in self.FILENAMES_MAPPING.items()]
            ax2.boxplot(boxes, notch=True, showmeans=True, meanprops=meanpointprops)
            ax2.yaxis.tick_right()
            plt.gca().invert_xaxis()
            ax2.grid(color='k', linewidth=.5, linestyle=':')
            ax2.set_ylim(60, 100)
            xtick_names = plt.setp(ax2, xticklabels=self.FILENAMES_MAPPING.values())
            plt.setp(xtick_names, rotation=45)

        # save results
        plt.savefig('5_star_plot.pdf')
        plt.close()


if __name__ == '__main__':
    graph = Graph()
    graph.run()
