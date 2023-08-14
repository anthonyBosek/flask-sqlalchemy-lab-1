# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here


@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()

    if not quake:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    else:
        body = quake.to_dict()
        status = 200

    return make_response(body, status)


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    quakes = []
    for quake in Earthquake.query.filter(Earthquake.magnitude >= magnitude).all():
        quakes.append(quake.to_dict())
    body = {'count': len(quakes),
            'quakes': quakes
            }
    return make_response(body, 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)