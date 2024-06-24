from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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