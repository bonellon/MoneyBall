from flask import Flask, request
import json


app = Flask(__name__)


@app.route('/')
def welcome():
    app.logger.info("Successfully invoked the index route")
    return "Welcome to Adaptive Itinerarizer"


@app.route('/suggest', methods=['POST'])
def suggest_places():
    '''app.logger.info(request.is_json)
    input_data = request.get_json()
    user_id, user_name, places = service.plan_trip(json.dumps(input_data))
    app.logger.info(user_id)
    app.logger.info(places)
    return jsonify(user_id=user_id, user_name=user_name, places=places)
    '''
    return "OII"
    # return str(input_data)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)