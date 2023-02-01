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
	return prediction, sentiment

app = Flask(__name__)
@app.route('/predict', methods=['GET', 'POST'])
def add_message():
    try:
        content = request.json
        prediction = int(predict([content['mytext']])[0])
        prediction = {"prediction": False} if prediction else {"prediction": True} 
        prediction['sentiment'] = None
        if not prediction["prediction"]:
            try:
                print("Using perfect predict...")
                perfect_predictin, sentiment = perfect_predict(content['mytext'])
                prediction['prediction'] = perfect_predictin
                prediction['sentiment'] = sentiment
                
            except Exception as e:
                print(e)

        return jsonify(prediction)
    except Exception as e: 
        print(e)
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
