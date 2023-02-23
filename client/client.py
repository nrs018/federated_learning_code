from receiveModel import receiveModel
from uploadModel import uploadModel
from localTraining import *

print('waiting model from server ....')
reModel = receiveModel()
reModel.receiveBroadcast()
print('start to train....')
localT = localTraining()
localT.training()
localT.saveModel()
print('start to upload the local model...')

upModel = uploadModel()
upModel.uploadModel()

print('Uploading model finished!')