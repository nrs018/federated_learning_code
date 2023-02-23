import torch
import os
import yaml
from src.utils import *
from collections import OrderedDict
from src.models import *
from torchsummary import summary
import pickle

class aggregateModel:
    def __init__(self, round):
        with open('./config.yaml') as c:
            configs = list(yaml.load_all(c, Loader=yaml.FullLoader))
        self.fed_config = configs[1]['fed_config']
        self.init_config = configs[3]['init_config']
        self.model_config = configs[4]['model_config']
        self.criterion = self.fed_config['criterion']
        self.path = './model/'
        self.round = round
        self.model = eval(self.model_config['name'])(**self.model_config)
        init_net(self.model, **self.init_config)
        self.model.load_state_dict(torch.load(self.path + 'globalModel.pt'))

    def evaluate_global_model(self):
        with open('./data/mnist_test.pickle', 'rb') as f:
            test = pickle.load(f)

        self.model.eval()
        test_loss, correct = 0, 0
        with torch.no_grad():
            for d, l in test:
                d = torch.reshape(d, [-1, 1, 28, 28])
                outputs = self.model(d)
                test_loss += eval(self.criterion)()(outputs, l).item()
                predicted = outputs.argmax(dim=1, keepdim=True)
                correct += predicted.eq(l.view_as(predicted)).sum().item()

        test_loss = test_loss / len(test)
        test_accuracy = correct / len(test)
        print('loss:', test_loss, ', accuracy:', test_accuracy)
        return test_loss, test_accuracy


    def aggregation(self):
        if not os.path.exists(self.path + 'round' + str(self.round)):
            os.mkdir(self.path + 'round' + str(self.round))

        averaged_weights = OrderedDict()
        all_model = []
        for f in os.listdir(self.path):
            if os.path.isfile(self.path + f):
                print(self.path + f)
                self.model.load_state_dict(torch.load(self.path + f))
                all_model.append(self.model.state_dict())

        w = 1.0 / len(all_model)
        for it in range(len(all_model)):
            local_weights = all_model[it]
            for key in local_weights.keys():
                if it == 0:
                    averaged_weights[key] = w * local_weights[key]
                else:
                    averaged_weights[key] += w * local_weights[key]
        self.model.load_state_dict(averaged_weights)
        # test_loss, test_acc = self.evaluate_global_model()

        if os.path.exists(self.path + 'globalModel.pt'):
            os.remove(self.path+'globalModel.pt')
        torch.save(self.model.state_dict(), self.path + 'globalModel.pt')
        os.system('mv ./model/globalModel.pt ./model/round' + str(self.round) + '/round' + str(self.round) + '.pt')
        for f in os.listdir(self.path):
            if os.path.isfile(self.path + f):
                os.system('mv ' + self.path + f + ' ./model/round' + str(self.round) + '/')
        os.system('cp ./model/round' + str(self.round) + '/round' + str(self.round) + '.pt ' +
                  './model/globalModel.pt')


