from src.models import *
import yaml
from src.utils import *
import torch
import pickle
import torch.utils.data

class localTraining:
    def __init__(self):
        with open('./config.yaml') as c:
            configs = list(yaml.load_all(c, Loader=yaml.FullLoader))
        self.data_config = configs[0]["data_config"]
        self.fed_config = configs[1]["fed_config"]
        self.optim_config = configs[2]["optim_config"]
        self.init_config = configs[3]["init_config"]
        self.model_config = configs[4]["model_config"]
        self.model = eval(self.model_config["name"])(**self.model_config)
        init_net(self.model, **self.init_config)
        self.model.load_state_dict(torch.load('./model/globalModel.pt'))

        self.optimizer = self.fed_config['optimizer']
        self.local_epoch = self.fed_config['E']
        self.batch_size = self.fed_config['B']
        self.criterion = self.fed_config['criterion']

    def training(self):
        with open('./data/mnist_train.pickle', 'rb') as f:
            train_data = pickle.load(f)

            data = []
            for i in range(len(train_data['train_data'])):
                data.append([train_data['train_data'][i]/255.0, train_data['train_label'][i]])
            trainloader = torch.utils.data.DataLoader(data,
                                                      shuffle=True,
                                                      batch_size=self.batch_size)
            self.model.train()
            self.model.to('cpu')
            optimizer = eval(self.optimizer)(self.model.parameters(), **self.optim_config)
            for e in range(self.local_epoch):
                global_loss = 0
                count = 0
                for d, labels in trainloader:
                    d = torch.reshape(d, [-1, 1, 28, 28]).type(torch.float)
                    optimizer.zero_grad()
                    outputs = self.model(d)
                    loss = eval(self.criterion)()(outputs, labels)
                    global_loss += loss.item()
                    loss.backward()
                    optimizer.step()
                    count += 1
                print('loss:', global_loss)

    def saveModel(self):
        torch.save(self.model.state_dict(), './model/localModel.pt')





