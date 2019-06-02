from setuptools import setup, find_packages

requires = [
    'pandas',
    'xlsxwriter',
]

setup(
    name='spmreport',
    version='0.1.0',
    description='Get report for SparkMeasure metrics in XLS format with graphs',
    author='McWladkoE',
    author_email='svevladislav@gmail.com',
    url='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=requires,
    entry_points="""\
        [console_scripts]
        spmreport_report = spmreport.report:main
    """,
)
