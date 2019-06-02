import os
import sys
import argparse

from collections import defaultdict
import pandas as pd

from .constants import (
    COLUMNS,
    SPLITTER,
    IGNORE_TESTS,
    COLUMNS_RANGE,
    LENGTH_BY_FOLDER,
)


class MetricsData:
    def __init__(self, input_path):
        self.data = defaultdict(dict)
        self.input_path = input_path

    def get_data_from_folder(self):
        file_list = os.listdir(self.input_path)

        for folder in file_list:
            path = os.path.join('results', folder)
            if not os.path.isdir(path):
                continue
            test_name = folder.split('_')[0]
            self.data[test_name] = defaultdict(dict)

            for key, val in COLUMNS.items():
                self.data[test_name][key][''] = val
            for file in os.listdir(path):
                name, ext = os.path.splitext(file)
                if name in IGNORE_TESTS:
                    continue
                if ext == '.out':
                    self.get_data_from_file(test_name, name, os.path.join(path, file))

    def get_data_from_file(self, test_name, name, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            started = False

            for i in lines[4:]:
                if i.startswith('Scheduling mode'):
                    started = True
                if started:
                    if not i or i == '\n' or i == SPLITTER or i == 'Aggregated Spark stage metrics:':
                        continue
                    splitted = i.split(' ')
                    if len(splitted) < 3:
                        print('Error parsing: {}'.format(i))
                        continue
                    if splitted[0] not in COLUMNS:
                        continue

                    try:
                        val = int(splitted[2].strip())
                    except TypeError:
                        val = splitted[2].strip()
                    self.data[test_name][splitted[0]][name] = val


def write_results(data, output_path):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    workbook = writer.book

    for folder, results in data.items():
        frame = pd.DataFrame(results)
        frame.to_excel(writer, sheet_name=folder)

        worksheet = writer.sheets[folder]
        for index, col in enumerate(COLUMNS_RANGE):
            chart = workbook.add_chart({'type': 'column'})
            chart.add_series({
                'values': '={sheet}!${col}$3:${col}${length}'.format(
                    sheet=folder,
                    col=col,
                    length=LENGTH_BY_FOLDER.get(folder) or 1
                ),
                'categories': '={sheet}!$A$3:$A${length}'.format(
                    sheet=folder,
                    length=LENGTH_BY_FOLDER.get(folder) or 1
                ),
                'name': '={sheet}!${col}$2'.format(sheet=folder, col=col),
                })
            chart.set_x_axis({'name': 'Имя Теста', 'rotate': 90})
            chart.set_legend({'position': 'none'})
            offset = index % 4
            if offset == 0:
                worksheet.insert_chart('A{}'.format(20 + (index // 4) * 15), chart)
            elif offset == 1:
                worksheet.insert_chart('I{}'.format(20 + (index // 4) * 15), chart)
            elif offset == 2:
                worksheet.insert_chart('Q{}'.format(20 + (index // 4) * 15), chart)
            elif offset == 3:
                worksheet.insert_chart('Y{}'.format(20 + (index // 4) * 15), chart)

    writer.save()


def main(argv=sys.argv):
    description = """
        Get report for SparkMeasure metrics in XLS format with graphs.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('input_path', metavar='input_path',
        help='Path to results folder')

    parser.add_argument('-o', '--output', dest='output_path',
        default='results.xlsx',
        help='Output file path')

    args = parser.parse_args(argv[1:])

    data = MetricsData(args.input_path)
    data.get_data_from_folder()

    if not data.data:
        print('Input data folder is empty or no data found.')
        return
    write_results(data.data, args.output_path)


if __name__ == '__main__':
    main()