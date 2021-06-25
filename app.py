
  
import flask
import pandas as pd
from joblib import dump, load


with open(f'models/randomForest.joblib', 'rb') as f:
    randomForest = load(f)


app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('index.html'))

    if flask.request.method == 'POST':
        age = flask.request.form['age']
        anaemia = flask.request.form['anaemia']
        creatine_phosphokinase = flask.request.form['creatine_phosphokinase']
        diabetes = flask.request.form['diabetes']
        ejection_fraction = flask.request.form['ejection_fraction']
        high_blood_pressure = flask.request.form['high_blood_pressure']
        platelets = flask.request.form['platelets']
        serum_creatinine = flask.request.form['serum_creatinine']
        serum_sodium = flask.request.form['serum_sodium']
        sex = flask.request.form['sex']
        smoking = flask.request.form['smoking']
        time = flask.request.form['time']

        input_variables = pd.DataFrame([[age,anaemia, creatine_phosphokinase, diabetes, ejection_fraction, high_blood_pressure, platelets, serum_creatinine, serum_sodium, sex, smoking, time]],
        columns=['age', 'anaemia', 'creatine_phosphokinase', 'diabetes', 'ejection_fraction', 'high_blood_pressure', 'platelets', 'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time' ],
        dtype='float',
        index=['input'])

        predictions = randomForest.predict(input_variables)[0]
        print(predictions,'WTF')

        return flask.render_template('index.html', original_input={'Age': age, 'Anaemia': anaemia, 'Creatine Phosphokinase': creatine_phosphokinase, 'Diabetes': diabetes, 'Ejection Fraction': ejection_fraction, 'High Blood Pressure': high_blood_pressure, 'Platelets': platelets, 'Serum Creatinine': serum_creatinine, 'Serum Sodium': serum_sodium, 'Sex': sex, 'Smoking': smoking, 'Time':time  },
                                     result=predictions)


if __name__ == '__main__':
    app.run(debug=True)