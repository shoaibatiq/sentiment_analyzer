from flask import Flask, request, jsonify
import requests
from sentiment_analyzer import predict

def perfect_predict(text):
	url = "https://perfect-sentiment-analysis.p.rapidapi.com/"

	querystring = {"string": text}

	headers = {
		"X-RapidAPI-Key": "7a7e4e4295mshcc423f46de64c10p1f57fcjsn2b872365896b",
		"X-RapidAPI-Host": "perfect-sentiment-analysis.p.rapidapi.com"
	}

	response = requests.get(url, headers=headers, params=querystring)
	response = response.json()
	sentiment = response['sentiment_analysis'].lower()
	prediction = sentiment[:3] not in [ 'neg', 'thr', 'hos']
	return prediction

app = Flask(__name__)
@app.route('/predict', methods=['GET', 'POST'])
def add_message():
    content = request.json
    prediction = int(predict([content['mytext']])[0])
    prediction = False if prediction else True
    if not prediction:
        try:
            print("Using perfect predict...")
            perfect_predictin = perfect_predict()
            prediction = perfect_predictin
        except:
            pass

    return jsonify({"prediction": prediction})

if __name__ == '__main__':
    app.run(debug=True)
