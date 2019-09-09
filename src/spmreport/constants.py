import string


class ResultField:
    def __init__(self, description, convert_to_sec=False):
        self.description = description
        self.convert_to_sec = convert_to_sec

    def get_converted_value(self, value):
        if not self.convert_to_sec:
            return value
        else:
            try:
                return round(int(value) / 1000., 3)
            except ValueError as e:
                print(e)


COLUMNS = {
    'sum(shuffleTotalBlocksFetched)': ResultField('Всего получено блоков(?)'),
    'sum(jvmGCTime)': ResultField('Время сборки мусора JWM, с'),
    'sum(memoryBytesSpilled)': ResultField('Утекло памяти (байт)'),
    'sum(numUpdatedBlockStatuses)': ResultField('Обновлено статусов блоков'),
    'sum(executorCpuTime)': ResultField(
        'Время CPU выполнения, c',
        convert_to_sec=True
    ),
    'sum(shuffleWriteTime)': ResultField(
        'Время записи передачи, c',
        convert_to_sec=True
    ),
    'sum(bytesRead)': ResultField('Прочитано байт'),
    'sum(bytesWritten)': ResultField('Записано байт'),
    'sum(shuffleRecordsWritten)': ResultField('Записано переданных записей'),
    'numStages': ResultField('Количество Этапов'),
    'max(resultSize)': ResultField('Размер результата'),
    'sum(shuffleLocalBlocksFetched)': ResultField(
        'Локальных блоков получено(?)',
        convert_to_sec=True
    ),
    'sum(resultSerializationTime)': ResultField(
        'Время сериализации результата, c',
        convert_to_sec=True
    ),
    'sum(executorRunTime)': ResultField(
        'Время выполнения, c',
        convert_to_sec=True
    ),
    'sum(shuffleBytesWritten)': ResultField('Записано переданных байт'),
    'elapsedTime': ResultField(
        'Затраченное время, c',
        convert_to_sec=True
    ),
    'sum(shuffleFetchWaitTime)': ResultField(
        'Время задержки получшения передачи, c',
        convert_to_sec=True
    ),
    'sum(executorDeserializeTime)': ResultField(
        'Время десериализации выполнения, c',
        convert_to_sec=True
    ),
    'sum(numTasks)': ResultField('Количество задач'),
    'sum(shuffleRemoteBlocksFetched)': ResultField(
        'Удаленных блоков получено(?)'
    ),
    'sum(recordsWritten)': ResultField('Записано записей'),
    'sum(stageDuration)': ResultField(
        'Продолжительность этапа, c',
        convert_to_sec=True
    ),
    'sum(shuffleTotalBytesRead)': ResultField(
        'Всего переданных байт прочитано'
    ),
    'max(peakExecutionMemory)': ResultField('Пиковая Память при выполнении'),
    'sum(executorDeserializeCpuTime)': ResultField(
        'CPU Время десеализации, c',
        convert_to_sec=True
    ),
    'sum(recordsRead)': ResultField('Прочитано записей'),
    'sum(diskBytesSpilled)': ResultField('Утекло байт дисковой памяти'),
}

SPLITTER = '-' * 68 + '\n'

COLUMNS_RANGE = list(string.ascii_uppercase[1:]) + ['AA', 'AB']

IGNORE_TESTS = [
    'pic',
    'chi-sq-mat',
    'kmeans',
    'chi-sq-gof',
    'gmm',
]

SUMMARY_FIELDS = [
    'sum(executorCpuTime)',
    # 'sum(shuffleFetchWaitTime)',
]
