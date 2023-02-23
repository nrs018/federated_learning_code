from broadcast import broadcastModel
from receiveUpload import receiveUpload
from aggregateModel import *
import pandas as pd
from itertools import chain
import time

ROUND = 1
for i in range(ROUND):
    one_round_time = time.time()
    broadcast = broadcastModel()
    broadcast.broadcastmodel()

    reUpload = receiveUpload()
    reUpload.setTime(time.time())
    reUpload.receiveUploadModel()

    aggregateM = aggregateModel(i)
    aggregateM.aggregation()
    print('round', i, ': comsumed time {:6.2f}'.format(time.time() - one_round_time))
    aggregateM.evaluate_global_model()





