import spacy
import torch, torchtext
nlp = spacy.load('en')
from flask import Flask, jsonify, request, redirect, render_template
import os, pickle
import torch.nn as nn
import torch.nn.functional as F
from training.train_resnet50 import train, test
app = Flask(__name__)
app.secret_key = "secret key"

S3_BUCKET = os.environ['S3_BUCKET'] if 'S3_BUCKET' in os.environ else 'ganji-capstone'

s3 = boto3.client('s3')



# inference
def predict_classifier(key):
    model_path = '/data/'+token+'.pth'
    print ("File exists:"+str(path.exists(model_path)))
    if path.exists(model_path) == False:
        return 'Model Not Available'
    test_file_path = key+'-'+'test'
    obj = s3.get_object(Bucket=S3_BUCKET,key=test_file_path)
    #contents = obj.decode('utf-8')
    #print('creating byte stream')
    bytestream = io.BytesIO(obj['Body'].read())
    model=torch.load('model_path')
    #data_dir = '/datadrive/FastAI/data/aerial_photos/train'
    #test_transforms = transforms.Compose([transforms.Resize(224),
    #                                  transforms.ToTensor(),
                                     #])
    #model.eval()
    input = bytestream.to(device)
    output = model(input)
    return output



app.config['MAX_CONTENT_LENGTH'] = 224 * 224
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = '/data/'


# define model
class classifier(nn.Module):

    # Define all the layers used in model
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim, n_layers, dropout):
        super().__init__()

        # Embedding layer
        self.embedding = nn.Embedding(vocab_size, embedding_dim)

        # LSTM layer
        self.encoder = nn.LSTM(embedding_dim,
                               hidden_dim,
                               num_layers=n_layers,
                               dropout=dropout,
                               batch_first=True)
        # try using nn.GRU or nn.RNN here and compare their performances
        # try bidirectional and compare their performances

        # Dense layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, text, text_lengths):
        # text = [batch size, sent_length]
        embedded = self.embedding(text)
        # embedded = [batch size, sent_len, emb dim]

        # packed sequence
        packed_embedded = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths.cpu(), batch_first=True)

        packed_output, (hidden, cell) = self.encoder(packed_embedded)
        # hidden = [batch size, num layers * num directions,hid dim]
        # cell = [batch size, num layers * num directions,hid dim]

        # Hidden = [batch size, hid dim * num directions]
        dense_outputs = self.fc(hidden)

        # Final activation function softmax
        output = F.softmax(dense_outputs[0], dim=1)

        return output

# Define hyperparameters
size_of_vocab = 4651
embedding_dim = 300
num_hidden_nodes = 100
num_output_nodes = 3
num_layers = 2
dropout = 0.2

# Instantiate the model
model = classifier(size_of_vocab, embedding_dim, num_hidden_nodes, num_output_nodes, num_layers, dropout = dropout)

# load weights and tokenizer

path = '/home/ubuntu/tweetsa/models/saved_weights.pt'
model.load_state_dict(torch.load(path));
model.eval();
tokenizer_file = open('/home/ubuntu/tweetsa/models/tokenizer.pkl', 'rb')
tokenizer = pickle.load(tokenizer_file)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# inference

def classify_tweet(token,tweet):

    # tokenize the tweet
    tokenized = [tok.text for tok in nlp.tokenizer(tweet)]
    # convert to integer sequence using predefined tokenizer dictionary
    indexed = [tokenizer[t] for t in tokenized]
    # compute no. of words
    length = [len(indexed)]
    # convert to tensor
    tensor = torch.LongTensor(indexed).to(device)
    # reshape in form of batch, no. of words
    tensor = tensor.unsqueeze(1).T
    # convert to tensor
    length_tensor = torch.LongTensor(length)
    # Get the model prediction
    prediction = model(tensor, length_tensor)

    _, pred = torch.max(prediction, 1)

    return pred.item()

# URL Routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/sentiment/predict', methods=['POST'])
def predict_sentiment():
    if request.method == 'POST':
        token = request.form['token']
        tweet = request.form['tweet']
        my_prediction = classify_tweet(token,tweet)
        return render_template('result.html', prediction=my_prediction)

@app.route('/sentiment/train', methods=['POST'])
def train_sentiment():
    if request.method == 'POST':
        token = request.form['token']
        my_prediction = train_tweet(token)
    return render_template('result.html', prediction=my_prediction)


@app.route('/classify/train', methods=['POST'])
def train():
    if request.method == 'POST':
        key = request.form['token']
        my_model_path = train(key)
    return render_template('result.html', prediction=my_model_path)

@app.route('/classify/predict', methods=['POST'])
def test():
    if request.method == 'POST':
        key = request.form['token']
        my_prediction = test(key)
    return render_template('result.html', prediction=my_prediction)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
