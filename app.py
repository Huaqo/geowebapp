from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bevoelkerung(db.Model):
    __tablename__ = 'bevoelkerung'
    region_code = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(100), nullable=False)
    total_population = db.Column(db.Integer, nullable=False)
    male_population = db.Column(db.Integer, nullable=False)
    female_population = db.Column(db.Integer, nullable=False)

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

class Hochschulen_Bevoelkerung(db.Model):
    __tablename__ = 'hochschulen_bevoelkerung'
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
    total_population = db.Column(db.Integer, nullable=False)
    male_population = db.Column(db.Integer, nullable=False)
    female_population = db.Column(db.Integer, nullable=False)


@app.route('/')
def home():
    bevoelkerung = Bevoelkerung.query.all()
    hochschulen = Hochschule.query.all()
    hochschulen_bevoelkerung = Hochschulen_Bevoelkerung.query.all()
    return render_template('index.html', bevoelkerung=bevoelkerung, hochschulen=hochschulen, hochschulen_bevoelkerung=hochschulen_bevoelkerung)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
