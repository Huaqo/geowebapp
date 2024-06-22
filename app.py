from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Hochschule(db.Model):
    __tablename__ = 'hochschulen'
    hochschulkurzname = db.Column(db.String(50), primary_key=True)
    hochschulname = db.Column(db.String(255))
    hochschultyp = db.Column(db.String(100))
    traegerschaft = db.Column(db.String(100))
    bundesland = db.Column(db.String(50))
    anzahl_studierende = db.Column(db.Integer)
    gruendungsjahr = db.Column(db.Integer)
    promotionsrecht = db.Column(db.Boolean)
    habilitationsrecht = db.Column(db.Boolean)
    strasse = db.Column(db.String(255))
    postleitzahl_hausanschrift = db.Column(db.Integer)
    ort_hausanschrift = db.Column(db.String(100))
    home_page = db.Column(db.String(255))

@app.route('/')
def home():
    hochschulen = Hochschule.query.all()
    return render_template('index.html', hochschulen=hochschulen)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
