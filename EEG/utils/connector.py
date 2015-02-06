__author__ = 'haohanwang'

import json
import os
import csv
import urllib2
import urllib
import sqlite3
import datetime
import pytz

tz = pytz.timezone('US/Eastern')
TIMEFORMAT = '%Y-%m-%d %H:%M:%S'

class DBDumper:
    '''
    initialize db host, userName, passWord, database name
    use getDataCSV() to extract
    '''
    def __init__(self, databaseName = 'database_name'):
        self.db = sqlite3.connect(databaseName)
        self.cursor = self.db.cursor()

    def getDataCSV(self, tableName, fileName, time_length=None):
        '''
        input tableName and fileName
        tableName is the name of that table to be extracted
        fileName is the name for the xls file, only 'eeg' and 'task'
        '''

        sql_select = 'select * from ' + tableName + ' as point '
        sql_where = ''

        if time_length is not None:
            d = datetime.datetime.now()
            d = tz.localize(d)
            d = d - datetime.timedelta(seconds=time_length)
            tstr = d.strftime(TIMEFORMAT)
            sql_where = 'where point.start_time > \'' + tstr + '\''


        sql = sql_select + sql_where
        print sql
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        header = [col[0] for col in self.cursor.description]

        text = []
        text.append(header)
        for item in results:
            line = []
            for i in range(len(item)):
                line.append(str(item[i]))
            text.append(line)
        writeCsv(fileName, text)


def writeCsv(fileName, data):
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, '../../EEG/static')
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, fileName+'.xls'), 'w') as f:
        w = csv.writer(f, delimiter = '\t')
        w.writerows(data)


def simulateTask(machine, subject, time_length):
    header = ['machine', 'subject', 'start_time', 'end_time', 'block', 'confusion']

    end_time = tz.localize(datetime.datetime.now())
    start_time = end_time - datetime.timedelta(seconds=time_length)
    end_time = end_time.strftime(TIMEFORMAT)
    start_time = start_time.strftime(TIMEFORMAT)
    row = [machine, subject, start_time, end_time, 'block', '-1']

    writeCsv('task.xls', [header, row])

class HttpRequestSender:
    def __init__(self, url, database = 'database_name'):
        self.url = url
        self.params = {}
        self.db = DBDumper(database)

    def postTrainRequest(self, currentAddress, task_table, eeg_table):
        self.db.getDataCSV(task_table, 'task')
        self.db.getDataCSV(eeg_table, 'eeg')
        self.params['eeg_file'] = currentAddress + '/static/eeg.xls'
        self.params['task_file'] = currentAddress + '/static/task.xls'
        post_data = [('q', self.compileJson()), ]
        result = urllib2.urlopen(self.url, urllib.urlencode(post_data))
        content = result.read()
        return content

    def postTestRequest(self, currentAddress, eeg_table, machine, subject, time_length):
        self.db.getDataCSV(eeg_table, 'eeg', time_length)
        simulateTask(machine, subject, time_length)
        self.params['eeg_file'] = currentAddress + '/static/eeg.xls'
        self.params['task_file'] = currentAddress + '/static/task.xls'
        post_data = [('q', self.compileJson()), ]
        result = urllib2.urlopen(self.url, urllib.urlencode(post_data))
        content = result.read()
        return content

    def getRequest(self):
        print self.url
        results = urllib2.urlopen(self.url)
        content = results.read()
        return content

    def setParams(self, params):
        for k, v in params.iteritems():
            self.params[k] = v

    def compileJson(self):
        return json.dumps(self.params)
