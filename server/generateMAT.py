
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
import pickle
import time
import numpy as np

BatchSize = 16
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
dataset1 = datasets.MNIST('../data', train=True, download=True,
                          transform=transform)
dataset2 = datasets.MNIST('../data', train=False,
                          transform=transform)

train_loader = torch.utils.data.DataLoader(dataset1)
test_loader = torch.utils.data.DataLoader(dataset2)

v_train, index_train = torch.sort(train_loader.dataset.targets)
v_test, index_test = torch.sort(test_loader.dataset.targets)

index = index_train[np.argwhere(v_train.numpy() < 5).reshape(-1)]
data01234 = {'train_data': train_loader.dataset.data[index], 'train_label': train_loader.dataset.targets[index]}

index = index_train[np.argwhere(v_train.numpy() >= 5).reshape(-1)]
data56789 = {'train_data': train_loader.dataset.data[index], 'train_label': train_loader.dataset.targets[index]}
# test_data = {'test_data': v_test, 'test_label': index_test}

print(train_loader.dataset.data[index][0])

file = open('./mnist_train01234.pickle', 'wb')
pickle.dump(data01234, file)
time.sleep(10)
file.close()

file = open('./mnist_train56789.pickle', 'wb')
pickle.dump(data56789, file)
time.sleep(10)
file.close()

file = open('./mnist_test.pickle', 'wb')
pickle.dump(test_loader, file)
time.sleep(10)
file.close()
print('finish')