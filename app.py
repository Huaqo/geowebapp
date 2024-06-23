from flask import Flask, render_template, send_file, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from tabulate import tabulate
from sqlalchemy import text
from queries import *

## CONFIG ##

template_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## MODELS ##

class Bevoelkerung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_bev = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=False)
    total_w = db.Column(db.Integer, nullable=False)
    total_m = db.Column(db.Integer, nullable=False)

class Bundesland(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_b = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=True)
    total_w = db.Column(db.Integer, nullable=True)
    total_m = db.Column(db.Integer, nullable=True)

class Regierungsbezirk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_r = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=True)
    total_w = db.Column(db.Integer, nullable=True)
    total_m = db.Column(db.Integer, nullable=True)
    bundesland_id = db.Column(db.Integer, db.ForeignKey('bundesland.id'), nullable=False)
    bundesland = db.relationship('Bundesland', backref=db.backref('regierungsbezirks', lazy=True))

class Landkreis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_l = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=True)
    total_w = db.Column(db.Integer, nullable=True)
    total_m = db.Column(db.Integer, nullable=True)
    regierungsbezirk_id = db.Column(db.Integer, db.ForeignKey('regierungsbezirk.id'), nullable=False)
    regierungsbezirk = db.relationship('Regierungsbezirk', backref=db.backref('landkreises', lazy=True))

class Stadt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_s = db.Column(db.String(100), nullable=False)
    total = db.Column(db.Integer, nullable=True)
    total_w = db.Column(db.Integer, nullable=True)
    total_m = db.Column(db.Integer, nullable=True)
    landkreis_id = db.Column(db.Integer, db.ForeignKey('landkreis.id'), nullable=False)
    landkreis = db.relationship('Landkreis', backref=db.backref('stadtes', lazy=True))

class Hochschulen(db.Model):
    namekurz_h = db.Column(db.String(50), nullable=False)
    name_h = db.Column(db.String(255), primary_key=True)
    typ = db.Column(db.String(100), nullable=True)
    traeger = db.Column(db.String(100), nullable=True)
    land = db.Column(db.String(50), nullable=True)
    studenten = db.Column(db.Integer, nullable=True)
    gjahr = db.Column(db.Integer, nullable=True)
    precht = db.Column(db.String(10), nullable=True)
    hrecht = db.Column(db.String(10), nullable=True)
    str = db.Column(db.String(255), nullable=True)
    plz = db.Column(db.Integer, nullable=True)
    ort = db.Column(db.String(100), nullable=True)
    web = db.Column(db.String(255), nullable=True)

## LOGIC ##

def gjahr_plot(order='ASC', limit=10):
    query = text(HOCHSCHULEN.format(order=order, limit=limit))
    result = db.session.execute(query)
    hochschulen = result.fetchall()
    names = [h.name_h for h in hochschulen]
    years = [h.gjahr for h in hochschulen]
    plt.figure(figsize=(10, 5))
    plt.barh(names, years, color='skyblue')
    plt.xlabel('Year')
    plt.ylabel('Name of Hochschule')
    plt.title('Top 10 Hochschulen by Year')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

def gjahr_table(order='ASC', limit=10, attributes=None):
    if not attributes:
        attributes = ['name_h']
    attributes = [attr for attr in attributes if attr]

    columns = ', '.join([f"h.{attr}" for attr in attributes])
    query = text(HOCHSCHULEN.format(order=order, limit=limit, columns=columns))
    result = db.session.execute(query)
    hochschulen = result.fetchall()
    table_data = [tuple(getattr(h, attr) for attr in attributes) for h in hochschulen]
    headers = [attr.capitalize() for attr in attributes]
    table = tabulate(table_data, headers=headers, tablefmt="html")
    return table


## ROUTING ##

@app.route('/')
def home():
    order = request.args.get('order', 'ASC')
    limit = request.args.get('limit', 10)
    try:
        limit = int(limit)
    except ValueError:
        limit = 10
    attributes = request.args.getlist('attributes')
    if not attributes:
        attributes = ['name_h']
    table = gjahr_table(order=order, limit=limit, attributes=attributes)
    return render_template('index.html', table=table, order=order, limit=limit, attributes=attributes)

@app.route('/gjahr_plot.png')
def gjahr_plot_route():
    img = gjahr_plot()
    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)