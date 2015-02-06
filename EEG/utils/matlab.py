from connector import HttpRequestSender

MY_ADDRESS = 'http://li282-60.members.linode.com'
MATLAB_ADDRESS = 'http://128.2.178.115:4000/'

def train():
    # TODO pull all these things into a config file
    hrs = HttpRequestSender(url=MATLAB_ADDRESS + 'train', database='db.sqlite3')
    self_serverAddress = MY_ADDRESS
    out = hrs.postTrainRequest(self_serverAddress, 'EEGtesting_confusiontask', 'EEGtesting_raw')
    return out

def test(classifier):
    # TODO pull all these things into a config file
    hrs = HttpRequestSender(url=MATLAB_ADDRESS + 'test', database='db.sqlite3')
    self_serverAddress = MY_ADDRESS
    hrs.setParams({'classifier': classifier})
    result_loc = hrs.postTestRequest(self_serverAddress, 'EEGtesting_raw', '11699', 'yiwei', 10)

    hrs2 = HttpRequestSender(url=MATLAB_ADDRESS + result_loc, database='db.sqlite3')
    results = hrs2.getRequest()
    return results
