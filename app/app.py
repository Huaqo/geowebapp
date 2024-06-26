from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from tabulate import tabulate
from sqlalchemy import text
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import os
import re
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from io import BytesIO
import base64
import time
import folium

## QUERIES

DATASET = """
SELECT {attributes}
FROM Hochschulen h
JOIN Bevoelkerung b ON b.region_name = h.ort 
AND b.bundesland = h.land 
AND (
    b.region_type = 'kreis' 
    OR b.region_name = 'Berlin' 
    OR b.region_name = 'Hamburg' 
    OR b.region_name = 'Bremen' 
    OR b.region_name = 'Hannover' AND b.region_type = 'landeshauptstadt' 
    OR b.region_name = 'Saarbrücken' AND b.region_type = 'landeshauptstadt')
AND {search_attr} ILIKE :search
ORDER BY {sort_by} {order}
LIMIT {limit};
"""


## INIT

db = SQLAlchemy()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

app = create_app()


## DATA QUERY 

class Dataset_Parameters:
    def __init__(self, order='ASC', limit='10', sort_by='gjahr', attributes=['name_h'], search='', search_attr='name_h'):
        if attributes is None:
            attributes = ['name_h']
        self.order = order
        self.limit = limit
        self.sort_by = sort_by
        self.attributes = attributes
        self.search = search
        self.search_attr = search_attr
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    @classmethod
    def get_parameters(cls, request):
        parameters = cls()
        parameters.update(
            order=request.args.get('order', parameters.order),
            limit=request.args.get('limit', parameters.limit),
            sort_by=request.args.get('sort_by', parameters.sort_by),
            attributes=request.args.getlist('attributes') or parameters.attributes,
            search=request.args.get('search', parameters.search),
            search_attr=request.args.get('search_attr', parameters.search_attr)
        )
        parameters.attributes = [attr for attr in parameters.attributes if attr]
        if 'lat' not in parameters.attributes:
            parameters.attributes.append('lat')
        if 'lon' not in parameters.attributes:
            parameters.attributes.append('lon')
        return parameters

def get_data(query_template, parameters):
    params_dict = {k: v for k, v in parameters.__dict__.items()}
    for key, value in params_dict.items():
        if isinstance(value, list):
            params_dict[key] = ', '.join(value)
    query = query_template.format(**params_dict)  
    result = db.session.execute(text(query), {'search': f"%{params_dict.get('search', '')}%"})
    print("Final query:", query)
    print("Search parameter:", f"%{parameters.search}%")
    print("Limit parameter:", parameters.limit)
    return result.fetchall()

## TABLE

def create_table(data, parameters):
    table_data = [list(row) for row in data]
    table = tabulate(table_data, headers=parameters.attributes, tablefmt='html')
    return table

## MAP
    
def generate_map(data, column_names):
    geolocator = Nominatim(user_agent="geoapiExercises")
    map_center = [51.1657, 10.4515]
    map = folium.Map(location=map_center, zoom_start=6)
    
    try:
        lat_index = column_names.index('lat')
        lon_index = column_names.index('lon')
    except ValueError:
        print("Lat or Lon column not found in the result set")
        return None

    for row in data:
        lat = row[lat_index]
        lon = row[lon_index]
        if lat is not None and lon is not None:
            folium.Marker([lat, lon], popup=f"Data: {row}").add_to(map)

    map_html = map._repr_html_()
    return map_html


## VIEWS

@app.route('/', methods=['GET'])
def home():
    dataset_parameters = Dataset_Parameters.get_parameters(request)
    dataset = get_data(DATASET, dataset_parameters)
    table = create_table(dataset, dataset_parameters)
    
    generate_map_flag = request.args.get('generate_map')
    map = None
    if generate_map_flag == "true":
        column_names = dataset_parameters.attributes
        map = generate_map(dataset, column_names)
    return render_template('index.html', table=table, parameters=dataset_parameters, map=map)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)