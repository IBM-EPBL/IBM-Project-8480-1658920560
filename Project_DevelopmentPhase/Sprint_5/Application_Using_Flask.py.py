import requests
from  flask import *
import pandas as pd

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "GgbMbG9DNUGFtfjqv_PkRSdpgOnNBonWDs7yKAp3SgRI"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


'''
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict', methods=['POST'])
def y_predict():
    
    cB = request.form["cB"]
    cy = request.form["cylinder"]
    disp = request.form["disp"]
    hP = request.form["hP"]
    weight = request.form["W"]
    Acc = request.form["Acc"]
    mY = request.form["mY"]
    origin = request.form["orgin"]
    
    t = [[11 , int(cy),int(disp),int(hP),int(weight),int(Acc),int(mY),int(origin)]]
    print(t)
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": ["car name" , "cylinders" , "displacement" ,"horsepower","weight" , "acceleration" ,"model year" ,"orgin"], "values": t}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2e34925b-a557-48a1-8d5e-b3bacfd6ded0/predictions?version=2022-11-18', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction = response_scoring.json()

    print(prediction)
    out = prediction['predictions'][0]['values'][0][0]

    return render_template('index.html' , prediction_text=out)

if( __name__ == "__main__"):
    app.run(debug = False)
'''  


app = Flask(__name__,template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/output',methods=['POST'])
def output():
    name = request.form['name']
    name = name.split(' ')[0]
    temp = pd.read_csv('Temp_file.csv')
    for i in range(len(temp["Brand"])):  
        if temp["Brand"].iloc[i] == name:
            name = temp["Encoded"].iloc[i]
    cyl = request.form['cylinder']
    disp = request.form['displacement']
    hp = request.form['hp']
    w = request.form['weight']
    acc = request.form['acceleration']       
    year = request.form['year']
    origin = request.form['origin']
    
    payload_scoring = {"input_data": [{"field": ["cylinders" , "displacement" ,"horsepower","weight" , "acceleration" ,"model year" ,"orgin","Brand"], "values":[[int(cyl) , int(disp),int(hp),int(w),int(acc),int(year),int(origin),int(name)]]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2e34925b-a557-48a1-8d5e-b3bacfd6ded0/predictions?version=2022-11-18', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    prediction = response_scoring.json()
    return render_template('output.html' , pred=prediction['predictions'][0]['values'][0][0])
app.run()  
    