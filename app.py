from flask import Flask, redirect, url_for, request, render_template
from sklearn.metrics import precision_score, recall_score
import pandas as pd
import numpy as np
import dill
import json
import requests

app = Flask(__name__)
#model path
model='nb_model.pkl'


#renders home page
@app.route("/")
def home():
    return render_template('home.html')



@app.route('/metrics/<n>')
def success(n):
    data = pd.read_csv('data.csv', nrows=int(n))
    test = data
    #load real value
    Y_test = np.array(test.AccountNumber)
    #load prediction
    res=np.array(test.Predicted)
    #create json structure
    x = {
        "precision": precision_score(Y_test, res, average='micro'),
        "recall": recall_score(Y_test, res, average='micro')
    }
    y = json.dumps(x)
    return y



@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        id = request.form['id']
        compId = request.form['cid']
        #load data file
        data = pd.read_csv('data.csv')
        #locate record
        data1=data.loc[(data['Unnamed: 0'] == int(id)) &(data['CompanyId'] == compId)]
        if (len(data1) == 0):
            return "record not found"
        else:
            #predict record
            loaded = dill.load(open(model, 'rb'))
            res = loaded.predict(data1)
            x = [{res[0]}]

            return str(x)
    else:
        return "error"




@app.route('/sample', methods=['POST'])
def sample():
    if request.method == 'POST':
        #load model
        loaded = dill.load(open(model, 'rb'))
        #recive data
        rec = pd.DataFrame(request.json)
        #predict for recived data
        predicted = loaded.predict(rec)
        rec['Predicted'] = predicted
        #load data
        data = pd.read_csv('data.csv')
        df_row = pd.concat([rec, data], ignore_index=True)
        #save recived + historic data
        df_row.to_csv('data.csv', index=False)
        #load new data
        train = pd.read_csv('data.csv')
        Y_train = train.AccountNumber
        # train model with new dat
        loaded.fit(train, Y_train)
        # save model
        dill.dump(loaded, open(model, 'wb'))
        return "done"
    else:
        return "error"



if __name__ == '__main__':
    app.run(debug=True)
