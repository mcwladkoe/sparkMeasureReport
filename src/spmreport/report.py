import os
import sys
import argparse

from datetime import datetime, timezone

import re

from collections import defaultdict
import pandas as pd
# import pandas.io.formats.excel as fmt_xl
import json

from .constants import (
    COLUMNS,
    SPLITTER,
    IGNORE_TESTS,
    COLUMNS_RANGE,
    SUMMARY_FIELDS,
)


class MetricsData:
    def __init__(self, input_path, calculate_cpu_congestion=False):
        self.data = defaultdict(dict)
        self.calculate_cpu_congestion = calculate_cpu_congestion
        self.start_date = 10**20
        self.end_date = 0
        self.initialize_test_data('decisiontree')
        self.input_path = input_path

    def initialize_test_data(self, test_name):
        self.data[test_name] = defaultdict(dict)
        for key, val in COLUMNS.items():
            self.data[test_name][key][''] = val.description

    def get_data_from_folder(self):
        file_list = os.listdir(self.input_path)

        for folder_name in file_list:
            path = os.path.join(self.input_path, folder_name)
            if not os.path.isdir(path):
                continue
            test_name = folder_name.split('_')[0]

            if self.calculate_cpu_congestion:
                date_str = re.findall(
                    r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}',
                    folder_name
                )[0]
                start_date = datetime.strptime(date_str, '%Y-%m-%d_%H-%M-%S') \
                    .replace(tzinfo=timezone.utc) \
                    .timestamp()
                self.start_date = min(self.start_date, start_date)

            self.initialize_test_data(test_name)
            for file in os.listdir(path):
                name, ext = os.path.splitext(file)
                file_path = os.path.join(path, file)
                if self.calculate_cpu_congestion:
                    stat = os.stat(file_path)
                    # stat.st_ctime
                    self.start_date = min(self.start_date, stat.st_mtime)
                    self.end_date = max(self.end_date, stat.st_mtime)
                if name in IGNORE_TESTS:
                    continue
                if ext == '.out':
                    self.get_data_from_file(
                        test_name,
                        name,
                        file_path
                    )

    def get_data_from_file(self, test_name, name, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

            file_parsed = [{}]
            idx = 0
            dt_num = 1

            counts = defaultdict(int)

            for i in lines:
                if i == SPLITTER:
                    idx += 1
                    file_parsed.append({})
                    continue
                splitted = i.split(' ')
                if splitted[0] == 'results:':
                    d = json.loads(' '.join(splitted[1:]))
                    if d['testName'] == 'decision-tree':
                        file_parsed[idx]['name'] = 'Dtr{}'.format(dt_num)
                        file_parsed[idx]['test'] = 'decisiontree'
                        dt_num += 1
                    else:
                        file_parsed[idx]['name'] = d['testName']
                        file_parsed[idx]['test'] = test_name
                    continue
                column = COLUMNS.get(splitted[0])
                if not column:
                    continue
                try:
                    val = int(splitted[2].strip())
                except TypeError:
                    val = splitted[2].strip()
                file_parsed[idx][splitted[0]] = column.get_converted_value(val)

            for line in file_parsed:
                if not line:
                    continue
                name = line.pop('name')
                if not name:
                    print("Error: {}".format(line))
                test = line.pop('test')

                test_name = name + test
                counts[test_name] += 1
                if counts[test_name] > 1:
                    name = '{}-{}'.format(name, counts[test_name])
                for k, v in line.items():
                    self.data[test][k][name] = v


def write_results(results_data, output_path, calculate_cpu_congestion=False):
    writer = pd.ExcelWriter(output_path, engine='xlsxwriter')
    workbook = writer.book
    data = results_data.data

    # fmt_xl.header_style = None
    fmt = writer.book.add_format({"font_name": "Times New Roman"})
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'border': 1,
        'font_name': 'Times New Roman'
    })

    for folder, results in data.items():
        frame = pd.DataFrame(results)
        if not folder:
            print(results)
            continue

        # frame.style.format({'B': "{:0<4.0f}", 'D': '{:+.2f}'})
        frame.to_excel(writer, sheet_name=folder, startrow=1, startcol=1, header=False, index=False)
        # frame.style.set_properties(**{"font_name": "Times New Roman"})
        data_length = len(frame.index) + 1

        worksheet = writer.sheets[folder]

        # Write the column headers with the defined format.
        for col_num, value in enumerate(frame.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)

        for row_num, value in enumerate(frame.index):
            worksheet.write(row_num + 1, 0, value, header_format)

        for index, col in enumerate(COLUMNS_RANGE):
            chart = workbook.add_chart({'type': 'column'})
            chart.add_series({
                'values': '={sheet}!${col}$3:${col}${length}'.format(
                    sheet=folder,
                    col=col,
                    length=data_length
                ),
                'categories': '={sheet}!$A$3:$A${length}'.format(
                    sheet=folder,
                    length=data_length
                ),
                'name': '={sheet}!${col}$2'.format(sheet=folder, col=col),
            })
            chart.set_x_axis({'name': 'Имя Теста', 'rotate': 90})
            chart.set_legend({'position': 'none'})
            offset = index % 4
            result_row_index = data_length + 4 + (index // 4) * 15
            worksheet.insert_chart(
                '{}{}'.format(chr(65 + offset * 8), result_row_index),
                chart
            )  # chr(65) = A
    if results_data.calculate_cpu_congestion:
        # in seconds
        print(results_data.start_date)
        totals_data = {
            'start_date': {
                'name': 'Дата старта',
                'val': results_data.start_date,
            },
            'end_date': {
                'name': 'Дата окончания',
                'val': results_data.end_date,
            },
            'timedelta': {
                'name': 'Время теста, с',
                'val': results_data.end_date - results_data.start_date,
            },
        }
        total_cpu_time = 0
        for _, results in data.items():
            for i in SUMMARY_FIELDS:
                executor_cpu_time_results = results[i]
                for k in executor_cpu_time_results.keys():
                    if k:
                        total_cpu_time += executor_cpu_time_results[k]
        totals_data['executorCpuTime'] = {
            'name': 'Время выполнения на executor\'ах',
            'val': total_cpu_time
        }
        totals_data.update({
            'instances': {
                'name': 'Количество executor\'ов',
                'val': 4,
            },
            'cpu_instance_time': {
                'name': 'Время для одного executor\'а',
                'val': '=D3/E3',
            },
            'cpu_congestion': {
                'name': 'Нагрузка для одного executor\'а',
                'val': '=F3/C3',
            }
        })

        frame = pd.DataFrame(totals_data)
        frame.to_excel(writer, sheet_name='totals', index=False)
        # print(results_data.end_date - results_data.start_date)
    for name, worksheet in writer.sheets.items():
        worksheet.set_column('A:AB', None, fmt)
        worksheet.set_row(0, None, fmt)

    writer.save()


def main(argv=sys.argv):
    description = """
        Get report for SparkMeasure metrics in XLS format with graphs.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        'input_path',
        metavar='input_path',
        help='Path to results folder'
    )

    parser.add_argument(
        '-o',
        '--output',
        dest='output_path',
        default='results.xlsx',
        help='Output file path'
    )

    args = parser.parse_args(argv[1:])

    data = MetricsData(args.input_path, calculate_cpu_congestion=True)
    data.get_data_from_folder()

    if not data.data:
        print('Input data folder is empty or no data found.')
        return
    write_results(data, args.output_path)


if __name__ == '__main__':
    main()
