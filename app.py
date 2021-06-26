

import flask
import pandas as pd
from joblib import load


with open(f'models/randomForest.joblib', 'rb') as f:
    randomForest = load(f)


app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':
        age = flask.request.form['age']
        sex = flask.request.form['sex']
        cp = flask.request.form['cp']
        trestbps = flask.request.form['trestbps']
        chol = flask.request.form['chol']
        fbs = flask.request.form['fbs']
        restecg = flask.request.form['restecg']
        thalach = flask.request.form['thalach']
        exang = flask.request.form['exang']
        oldpeak = flask.request.form['oldpeak']
        slope = flask.request.form['slope']
        ca = flask.request.form['ca']
        thal = flask.request.form['thal']

        input_variables = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                                       columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                                                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'],
                                       dtype='float',
                                       index=['input'])
        predictions = randomForest.predict(input_variables)[0]

    return flask.render_template('index.html', original_input={'Age': age, 'Sex': sex, 'Chest Pain': cp, 'Trestbps': trestbps, 'Cholestrol Amount': chol, 'FBS': fbs, 'Restecg': restecg, 'Thalach': thalach, 'Exang': exang, 'Old Peak': oldpeak, 'Slope': slope, 'CA': ca, 'Thal': thal},
                                 result=predictions)


if __name__ == '__main__':
    app.run(debug=True)
