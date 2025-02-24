#from flask.ext.api import FlaskAPI
from flask import request, current_app, abort
from functools import wraps
#from flask import request, url_for, current_app, abort
from flask_api import FlaskAPI


app = FlaskAPI(__name__)
app.config.from_object('settings')


def token_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-TOKEN', None) != current_app.config['API_TOKEN']:
            abort(403)
        print ("auth ok")
        return f(*args, **kwargs)
    return decorated_function


@app.route('/predict', methods=['POST'])
@token_auth
def predict():
    from engines import content_engine
    item = request.data.get('item')
    num_predictions = request.data.get('num', 10)
    print ("(item,num_predictions):",item, num_predictions)
    if not item:
        return []
    return content_engine.predict(str(item), num_predictions)


@app.route('/train')
@token_auth
def train():
    from engines import content_engine
    data_url = request.data.get('data-url', None)
    content_engine.train(data_url)
    return {"message": "Success!", "success": 1}


if __name__ == '__main__':
    app.debug = True
    app.run()
