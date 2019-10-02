from flask import Flask
from models.actors import Actor

app = Flask(__name__)

@app.route('/actors/<string:name>')
def get_actor_by_name(name):
    try:
        actor = Actor(name)
        return actor.dict()
    except AttributeError:
        return 'No existen actores con ese nombre'
    
if __name__ == '__main__':
    app.run(debug=True)
