import os
import pathlib
import requests
from flask import Flask, session, abort, redirect, request, render_template
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import pandas as pd
from joblib import load


with open(f'models/randomForest.joblib', 'rb') as f:
    randomForest = load(f)



app = Flask("Heart Failure Prediction & Prevention System")
app.secret_key = "Heart Failure Prediction & Prevention System"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "927998997363-s7p33c44tajcdh8s0sfredhnaudrso8s.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/predict")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/protected_area")
@login_is_required
def protected_area():
    return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"


#Define functions for translating variables to human understandale language
def translate_predictions(variable):
    if variable == 1 :
        return "Positive"
    else :
        return "Negative"

def translate_sex(variable):
    if variable == 1 :
        return "Male"
    else :
        return "Female"

def translate_chest_pains(variable):
    if variable == 0 :
        return "None"
    elif variable == 1:
        return "Moderate"
    elif variable == 2 :
        return "Intense"
    else :
        return "Extreme"

def translate_multi(variable):
    if variable == 0 :
        return "Low"
    elif variable == 1:
        return "Moderate"
    else :
        return "High"

def translate_exang(variable):
    if variable == 0 :
        return "Low"
    else :
        return "High"

#Prediction routes
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return (render_template('home.html', user={session['name']}))

    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']

        input_variables = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                                       columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                                                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'],
                                       dtype='float',
                                       index=['input'])
        predictions = randomForest.predict(input_variables)[0]
        
        # Translate variables to human readable and understandable format
        translated_predictions = translate_predictions(predictions)
        translated_fbs = translate_predictions(fbs)
        translated_sex = translate_sex(sex)
        translated_chest_pains = translate_chest_pains(cp)
        translated_exang = translate_exang(exang)
        translated_ca = translate_multi(ca)
        translated_thal = translate_multi(thal)
        translated_restecg = translate_multi(restecg)
        translated_slope = translate_multi(slope)

    return render_template('home.html', original_input={'Age': age, 'Sex': translated_sex, 'Chest Pain': translated_chest_pains, 'Trestbps': trestbps, 'Cholestrol Amount': chol, 'FBS': translated_fbs, 'Restecg': translated_restecg, 'Thalach': thalach, 'Exang': translated_exang, 'Old Peak': oldpeak, 'Slope': translated_slope, 'CA': translated_ca, 'Thal': translated_thal},
                                 result=translated_predictions)

if __name__ == '__main__':
    app.run(debug=True)

