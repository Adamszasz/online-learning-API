#client app to call API

import json
import requests
import pandas as pd

#api urls
api_metrics = 'http://localhost:5000/metrics/10'
api_sample = 'http://localhost:5000/sample'
api_predict = 'http://localhost:5000/predict'
data = {'id': '1', 'cid': 'int:a055470'}
# source of data
recived = pd.read_csv('bank_expenses_obfuscated.csv')
rj=recived.to_json(orient='records')
rj=json.loads(rj)
print('data loaded')


step=100
for n in range(0, 5*step, step):
    r = requests.post(url=api_sample, json=rj[n:n+step])
    print('Sample: ', r.status_code, r.reason, r.text)
    r = requests.get(url=api_metrics)
    print('Metrics: ', r.status_code, r.reason, r.text)
    r = requests.post(url=api_predict, data=data)
    print('Prediction: ', r.status_code, r.reason, r.text)


print('finish')
