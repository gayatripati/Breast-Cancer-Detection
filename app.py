from flask import Flask,render_template,request
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


app = Flask(__name__)


@app.route('/',methods=["GET","POST"])
def prob():

	if request.method == 'POST':

		formValues = dict(request.form)

		default = {  
					 'radius_mean': 14.127291739894563,
					 'perimeter_mean': 91.96903339191566,
					 'area_mean': 654.8891036906857,
					 'compactness_mean': 0.10434098418277686,
					 'concavity_mean': 0.08879931581722322,
					 'concave points_mean': 0.048919145869947236,
					 'radius_se': 0.4051720562390161,
					 'perimeter_se': 2.8660592267135288,
					 'area_se': 40.33707908611603,
					 'radius_worst': 16.269189806678394,
					 'perimeter_worst': 107.2612126537786,
					 'area_worst': 880.5831282952545,
					 'compactness_worst': 0.25426504393673144,
					 'concavity_worst': 0.27218848330404205,
					 'concave points_worst': 0.11460622319859404

					 }


		print(formValues)

		flag = False
		for key in formValues:

			if formValues[key] == '':

				formValues[key] = default[key]

			else:

				formValues[key] = float(formValues[key][0])
				flag = True


		if flag:

			inputValues = [list(formValues.values())]

			model = pickle.load(open('model.pkl', 'rb'))

			result = model.predict_proba(inputValues)[0]

			if result[0] > result[1]:

				output = ['Begnin', round(result[0], 2) * 100]
				output = f"The result is {output[0]} with the probability of {output[1]} %"

			elif result[1] > result[0]:

				output = ['Malignant', round(result[1], 2) * 100]
				output = f"The result is {output[0]} with the probability of {output[1]} %"

		else:

			output = 'Enter atleast 1 input and try again!!'

		return render_template('index.html', output = output)

	return render_template('index.html', output = False)



if __name__ == "__main__":

	app.run(debug=True)
