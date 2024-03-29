from Statistics.Historical import Evaluator as ev
from WEB import Formation as formation
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json


def init():
    import os
    if not os.path.isfile('gameweeks.json'):
        gameweeks = {}
        for i in range(1,39):
            svm = formation.Model("svm", [], [], [], [])
            rf = formation.Model("rf", [], [], [], [])
            gbm = formation.Model("gbm", [], [], [], [])

            newGW = formation.Formation(i, svm.__dict__, rf.__dict__, gbm.__dict__)

            gameweeks[i] = newGW.__dict__

        with open('gameweeks.json', 'w', encoding='utf-8') as file:
            json.dump(gameweeks, file, ensure_ascii=False, indent=2)


app = Flask(__name__)
CORS(app, support_credentials=True)
init()


@app.route('/summary')
def summary():
    response = app.response_class(
        response= json.dumps({
            "username":"admin",
            "email":"admin@aol.com",
            "id":"admin1"}
        ),
        status=200,
        mimetype='application/json'
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

'''
Store all previous data in json file. If json has output, return that otherwise use model to get predictions.
'''
@app.route('/predict/<gw>/<model>', methods=['GET'])
@cross_origin(supports_credentials=True)
def predict(gw, model):
    app.logger.info("Predicting Gameweek: "+str(gw))

    with open('gameweeks.json', 'r') as file:
        currentStore = json.load(file)

    if len(currentStore[str(gw)][model]["goalkeepers"]) > 0 and len(currentStore[str(gw)][model]["defenders"]) > 0:
        return jsonify(currentStore[str(gw)])

    result = ev.predict(int(gw), model)
    players = result[2]

    keeper = players[0]
    defenders = players[1]
    midfielders = players[2]
    forward = players[3]

    currentStore[str(gw)][model] = formation.Model(model, keeper, defenders, midfielders, forward).__dict__
    with open('gameweeks.json', 'w') as file:
        json.dump(currentStore, file, ensure_ascii=False, indent=2)




    return jsonify(result[2])



# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)
    init()