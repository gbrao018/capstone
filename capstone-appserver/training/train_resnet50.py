import spacy
import torch, torchtext
#nlp = spacy.load('en')
from flask import Flask, jsonify, request, redirect, render_template
import os, pickle
import torch.nn as nn
import torch.nn.functional as F
import boto3
import io
import json, base64, uuid, zipfile
#import cv2
#%matplotlib inline
#%config InlineBackend.figure_format = 'retina'
#import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch import optim
from torchvision import datasets, transforms, models
from torch.utils.data.sampler import SubsetRandomSampler
import os.path
from os import path
import torch.optim as optim
import zipfile
# define optimizer and loss
#optimizer = optim.Adam(model.parameters(), lr=2e-4)
#criterion = nn.CrossEntropyLoss()


app = Flask(__name__)
app.secret_key = "secret key"

S3_BUCKET = os.environ['S3_BUCKET'] if 'S3_BUCKET' in os.environ else 'ganji-capstone'

s3 = boto3.client('s3')

train_transforms = transforms.Compose([transforms.Resize(224),
    transforms.ToTensor(),])
test_transforms = transforms.Compose([transforms.Resize(224),
    transforms.ToTensor(),])


def load_split_train_test(datadir, valid_size = .2):
    train_transforms = transforms.Compose([transforms.Resize(224),
                                       transforms.ToTensor(),
                                       ])
    test_transforms = transforms.Compose([transforms.Resize(224),
                                      transforms.ToTensor(),
                                      ])
    train_data = datasets.ImageFolder(datadir,       
                    transform=train_transforms)
    test_data = datasets.ImageFolder(datadir,
                    transform=test_transforms)
    num_train = len(train_data)
    indices = list(range(num_train))
    split = int(np.floor(valid_size * num_train))
    np.random.shuffle(indices)
    from torch.utils.data.sampler import SubsetRandomSampler
    train_idx, test_idx = indices[split:], indices[:split]
    train_sampler = SubsetRandomSampler(train_idx)
    test_sampler = SubsetRandomSampler(test_idx)
    trainloader = torch.utils.data.DataLoader(train_data,
                   sampler=train_sampler, batch_size=8)
    testloader = torch.utils.data.DataLoader(test_data,
                   sampler=test_sampler, batch_size=8)
    return trainloader, testloader

def pretrain(key):
    obj = s3.get_object(Bucket=S3_BUCKET,key=token)
    #contents = obj.decode('utf-8')
    #print('creating byte stream')
    bytestream = io.BytesIO(obj['Body'].read())
    zfile = zipfile.ZipFile(bytestream)
    basedir = '/data'+key+'/'

    #file_list = [( name,
    #    basedir + os.path.basename(name),token + os.path.basename(name))
    #    for name in zfile.namelist()]

    with zipfile.ZipFile(bytestream, 'r') as zip_ref:
        zip_ref.extractall(basedir)

    #file_list = os.listdir(basedir)

    # resize the images
    #for (i, imagePath) in enumerate file_list:
    #    image = cv2.imread(imagePath)
    #    fil = basename(imagePath)
    #    filname = os.path.splitext(fil)[0]
    #    newimage = imutils.resize(image, width=120)
    #    cv2.imwrite(filname+'.jpg', newimage)
    # split test and train
    #data_dir = '/data/'+key
    #trainloader, testloader = load_split_train_test(data_dir, .2)
    #print(trainloader.dataset.classes)
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = models.resnet50(pretrained=True)
    print(model)
     ##First, we have to freeze the pre-trained layers, so we don’t backprop through them during training. Then, we re-define the final fully-connected the layer, the one that we’ll train with our images. We also create the criterion (the loss function) and pick an optimizer (Adam in this case) and learning rate.
    for param in model.parameters():
        param.requires_grad = False
    model.fc = nn.Sequential(nn.Linear(2048, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, 10),
            nn.LogSoftmax(dim=1))
    #criterion = nn.NLLLoss()
    #optimizer = optim.Adam(model.fc.parameters(), lr=0.003)
    #model.to(device)
    return model


def train(key):
    data_dir = '/data/'+key

    trainloader, testloader = load_split_train_test(data_dir, .2)
    print(trainloader.dataset.classes)
    
    model = pretrain(key)
    ##Now train the model
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.003)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    epochs = 2
    steps = 0
    running_loss = 0
    print_every = 10
    train_losses, test_losses = [], []
    criterion = nn.NLLLoss()
    optimizer = optim.Adam(model.fc.parameters(), lr=0.003)
    model.to(device)

    for epoch in range(epochs):
        for inputs, labels in trainloader:
            steps += 1
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            logps = model.forward(inputs)
            loss = criterion(logps, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            if steps % print_every == 0:
                test_loss = 0
                accuracy = 0
                model.eval()
                with torch.no_grad():
                    for inputs, labels in testloader:
                        inputs, labels = inputs.to(device),labels.to(device)
                        logps = model.forward(inputs)
                        batch_loss = criterion(logps, labels)
                        test_loss += batch_loss.item()
                        ps = torch.exp(logps)
                        top_p, top_class = ps.topk(1, dim=1)
                        equals = top_class == labels.view(*top_class.shape)
                        accuracy += torch.mean(equals.type(torch.FloatTensor)).item()
                        train_losses.append(running_loss/len(trainloader))
                        test_losses.append(test_loss/len(testloader))
                        print(f"Epoch {epoch+1}/{epochs}.. "
                                f"Train loss: {running_loss/print_every:.3f}.. "
                                f"Test loss: {test_loss/len(testloader):.3f}.. "
                                f"Test accuracy: {accuracy/len(testloader):.3f}")
                        running_loss = 0
                        model.train()
    model_save_path = '/data/'+key+'.pth'
    torch.save(model, model_save_path)
    return model_save_path

def predict_image(image,key):
    test_transforms = transforms.Compose([transforms.Resize(224),
        transforms.ToTensor(),])

    image_tensor = test_transforms(image).float()
    image_tensor = image_tensor.unsqueeze_(0)
    input = Variable(image_tensor)
    input = input.to(device)
    model_path = '/data'+key+'.pth'

    output = model(input)
    index = output.data.cpu().numpy().argmax()
    return index

# URL Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/classify/train', methods=['POST'])
def train():
    if request.method == 'POST':
        key = request.form['token']
        my_model_path = train(key)
    return render_template('result.html', prediction=my_model_path)

@app.route('/classify/test', methods=['POST'])
def test():
    if request.method == 'POST':
        key = request.form['token']
        my_prediction = test(key)
    return render_template('result.html', prediction=my_prediction)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
