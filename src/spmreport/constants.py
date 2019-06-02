import string


COLUMNS = {
    'sum(shuffleTotalBlocksFetched)': u'Всего получено блоков(?)',
    'sum(jvmGCTime)': u'Время сборки мусора JWM',
    'sum(memoryBytesSpilled)': u'Утекло памяти (байт)',
    'sum(numUpdatedBlockStatuses)': u'Обновлено статусов блоков',
    'sum(executorCpuTime)': u'Время CPU выполнения',
    'sum(shuffleWriteTime)': 'Время записи передачи',
    'sum(bytesRead)': 'Прочитано байт',
    'sum(bytesWritten)': 'Записано байт',
    'sum(shuffleRecordsWritten)': 'Записано переданных записей',
    'numStages': 'Количество Этапов',
    'max(resultSize)': u'Размер результата',
    'sum(shuffleLocalBlocksFetched)': 'Локальных блоков получено(?)',
    'sum(resultSerializationTime)': u'Время сериализации резултатата',
    'sum(executorRunTime)': 'Время выполнения',
    'sum(shuffleBytesWritten)': 'Записано переданных байт',
    'elapsedTime': 'Затраченное время',
    'sum(shuffleFetchWaitTime)': 'Время задержки получшения передачи',
    'sum(executorDeserializeTime)': 'Время десериализации выполнения',
    'sum(numTasks)': 'Количество задач',
    'sum(shuffleRemoteBlocksFetched)': 'Удаленных блоков получено(?)',
    'sum(recordsWritten)': 'Записано записей',
    'sum(stageDuration)': 'Продолжительность этапа',
    'sum(shuffleTotalBytesRead)': 'Всего переданных байт прочитано',
    'max(peakExecutionMemory)': 'Пиковая Память при выполнении',
    'sum(executorDeserializeCpuTime)': 'CPU Время десеализации',
    'sum(recordsRead)': 'Прочитано записей',
    'sum(diskBytesSpilled)': 'Утекло байт дисковой памяти',
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

LENGTH_BY_FOLDER = {
    'mllib': 18,
    'spark': 1,
}
