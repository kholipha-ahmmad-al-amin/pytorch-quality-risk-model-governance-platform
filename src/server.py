from flask import Flask,jsonify,request
from domain import ModelGovernance,DomainError
app=Flask(__name__);gov=ModelGovernance()
def actor():return {'role':request.headers.get('X-Role','viewer')}
@app.errorhandler(DomainError)
def error(e):return jsonify({'error':str(e)}),400
@app.post('/api/train')
def train():return jsonify({'loss':gov.train(actor()),'status':gov.status})
@app.post('/api/approve')
def approve():return jsonify({'status':gov.approve(actor())})
@app.post('/api/predict')
def predict():return jsonify({'risk':gov.predict((request.get_json() or {}).get('features'))})
@app.get('/api/status')
def status():return jsonify({'status':gov.status,'audits':gov.audits})
if __name__=='__main__':app.run(host='0.0.0.0',port=13200)
