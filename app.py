from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from tabulate import tabulate
from sqlalchemy import text
import folium
import os
from decimal import Decimal

## INIT
db = SQLAlchemy()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://huaqo:0000@localhost:5432/geowebapp')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
def create_app():
    template_dir = os.path.abspath('.')
    app = Flask(__name__,template_folder=template_dir)
    app.config.from_object(Config)
    db.init_app(app)
    return app
app = create_app()

## QUERIES
DATASET = """
SELECT {attributes}
FROM Hochschulen h
JOIN Mieten m ON m.land = h.land
LEFT JOIN Bevoelkerung b ON b.region_name = h.ort 
AND b.bundesland = h.land 
AND (
    b.region_type = 'kreis' 
    OR b.region_name = 'Berlin' 
    OR b.region_name = 'Hamburg' 
    OR b.region_name = 'Bremen' 
    OR b.region_name = 'Hannover' AND b.region_type = 'landeshauptstadt' 
    OR b.region_name = 'Saarbrücken' AND b.region_type = 'landeshauptstadt')
WHERE {search_attr} ILIKE :search
ORDER BY {sort_by} {order}
LIMIT {limit};
"""
DATASET_GROUPED = """
SELECT {group_by}, COUNT(*) AS Anzahl
FROM Hochschulen
GROUP BY {group_by}
ORDER BY Anzahl DESC;
"""

## PARAMETERS
order_by_options = [
    {'value': 'land', 'label': 'Bundesland'},
    {'value': 'typ', 'label': 'Hochschultyp'},
    {'value': 'traeger', 'label': 'Träger'},
    {'value': 'precht', 'label': 'Promotionsrecht'},
    {'value': 'hrecht', 'label': 'Habilitationsrecht'}
]

shortcut_options = [
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=ASC&sort_by=gjahr&limit=10&attributes=&attributes=h.name_h&attributes=h.gjahr&attributes=h.ort&generate_map=true', 'label': 'Älteste Hochschulen in Deutschland'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=DESC&sort_by=gjahr&limit=10&attributes=&attributes=h.name_h&attributes=h.gjahr&attributes=h.ort&generate_map=true', 'label': 'Jüngste Hochschulen in Deutschland'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=DESC&sort_by=studenten&limit=10&attributes=&attributes=h.name_h&attributes=h.studenten&attributes=h.ort&generate_map=true', 'label': 'Hochschulen mit den meisten Studenten'},
    {'url': '//127.0.0.1:5000/?search_attr=h.land&search=Berlin&order=DESC&sort_by=studenten&limit=10&attributes=&attributes=h.name_h&attributes=h.studenten&generate_map=true', 'label': 'Berliner Hochschulen mit den meisten Studenten'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=ASC&sort_by=studenten&limit=10&attributes=&attributes=h.name_h&attributes=h.studenten&attributes=h.ort&generate_map=true', 'label': 'Hochschulen mit den wenigsten Studenten'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=DESC&sort_by=b.total_population&limit=10&attributes=&attributes=h.name_h&attributes=h.ort&attributes=b.total_population&generate_map=true', 'label': 'Hochschulen mit den meisten Einwohnern'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=ASC&sort_by=b.total_population&limit=10&attributes=&attributes=h.name_h&attributes=h.ort&attributes=b.total_population&generate_map=true', 'label': 'Hochschulen mit den wenigsten Einwohnern'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=ASC&sort_by=m.mieten_ab_2019&limit=100&attributes=&attributes=h.name_h&attributes=h.ort&attributes=m.mieten_ab_2019&generate_map=true', 'label': 'Hochschulen mit den niedrigsten Mieten'},
    {'url': '//127.0.0.1:5000/?search_attr=typ&search=&order=DESC&sort_by=m.mieten_ab_2019&limit=200&attributes=&attributes=h.name_h&attributes=h.ort&attributes=m.mieten_ab_2019&generate_map=true', 'label': 'Hochschulen mit den höchsten Mieten'}
]

search_options = [
    {'value': 'h.name_h', 'label': 'Hochschulname'},
    {'value': 'h.typ', 'label': 'Typ'},
    {'value': 'h.traeger', 'label': 'Träger'},
    {'value': 'h.land', 'label': 'Land'},
    {'value': 'h.precht', 'label': 'Precht'},
    {'value': 'h.hrecht', 'label': 'Hrecht'},
    {'value': 'h.str', 'label': 'Straße'},
    {'value': 'h.ort', 'label': 'Ort'},
    {'value': 'h.web', 'label': 'Web'}
]

order_options = [
    {'value': 'ASC', 'label': 'Aufsteigend'},
    {'value': 'DESC', 'label': 'Absteigend'}
]

sort_by_options = [
    {'value': 'name_h', 'label': 'Hochschulname'},
    {'value': 'gjahr', 'label': 'Gründungsjahr'},
    {'value': 'typ', 'label': 'Typ'},
    {'value': 'traeger', 'label': 'Träger'},
    {'value': 'land', 'label': 'Land'},
    {'value': 'studenten', 'label': 'Studenten'},
    {'value': 'precht', 'label': 'Precht'},
    {'value': 'hrecht', 'label': 'Hrecht'},
    {'value': 'plz', 'label': 'PLZ'},
    {'value': 'str', 'label': 'Straße'},
    {'value': 'ort', 'label': 'Ort'},
    {'value': 'b.total_population', 'label': 'Einwohner'},
    {'value': 'm.mieten_ab_2019', 'label': 'Mieten'}
]

checkbox_options = [
    {'value': 'h.name_h', 'label': 'Hochschulname'},
    {'value': 'h.gjahr', 'label': 'Gründungsjahr'},
    {'value': 'h.typ', 'label': 'Typ'},
    {'value': 'h.traeger', 'label': 'Träger'},
    {'value': 'h.land', 'label': 'Land'},
    {'value': 'h.studenten', 'label': 'Studenten'},
    {'value': 'h.precht', 'label': 'Precht'},
    {'value': 'h.hrecht', 'label': 'Hrecht'},
    {'value': 'h.plz', 'label': 'PLZ'},
    {'value': 'h.str', 'label': 'Straße'},
    {'value': 'h.ort', 'label': 'Ort'},
    {'value': 'h.web', 'label': 'Web'},
    {'value': 'b.total_population', 'label': 'Einwohner'},
    {'value': 'm.mieten_ab_2019', 'label': 'Mieten'}
]

## DATA QUERY 
class Dataset_Parameters:
    def __init__(self, order='ASC', limit='10', sort_by='gjahr', attributes=['name_h'], search='', search_attr='name_h', group_by='typ'):
        if attributes is None:
            attributes = ['name_h']
        self.order = order
        self.limit = limit
        self.sort_by = sort_by
        self.attributes = attributes
        self.search = search
        self.search_attr = search_attr
        self.group_by = group_by
    
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
            search_attr=request.args.get('search_attr', parameters.search_attr),
            group_by=request.args.get('group_by', parameters.group_by)
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

    return result.fetchall()

## TABLES
def create_table(data, parameters):
    lat_index = parameters.attributes.index('lat') if 'lat' in parameters.attributes else -1
    lon_index = parameters.attributes.index('lon') if 'lon' in parameters.attributes else -1

    filtered_data = []
    for row in data:
        filtered_row = [value for i, value in enumerate(row) if i not in [lat_index, lon_index]]
        filtered_data.append(filtered_row)

    filtered_attributes = [attr for attr in parameters.attributes if attr not in ['lat', 'lon']]
    table = tabulate(filtered_data, headers=filtered_attributes, tablefmt='html')
    return table
def create_grouped_table(data, parameters):
    headers = [parameters.group_by, 'Anzahl']
    table = tabulate(data, headers=headers, tablefmt='html')
    return table

## MAP
def generate_map(data, column_names):
    map_center = [51.1657, 10.4515]
    map = folium.Map(location=map_center, tiles="cartodb positron", zoom_start=6)
    
    try:
        lat_index = column_names.index('lat')
        lon_index = column_names.index('lon')
    except ValueError:
        print("Lat or Lon column not found in the result set")
        return None
    
    bounds = []
    for row in data:
        lat = row[lat_index]
        lon = row[lon_index]
        if isinstance(lat, Decimal):
            lat = float(lat)
        if isinstance(lon, Decimal):
            lon = float(lon)
        if lat is not None and lon is not None:
            folium.Marker([lat, lon], popup=f"Data: {row}").add_to(map)
            bounds.append([lat, lon])

    if bounds:
        map.fit_bounds(bounds)

    map_html = map._repr_html_()
    return map_html

## VIEWS
@app.route('/', methods=['GET'])
def home():
    dataset_parameters = Dataset_Parameters.get_parameters(request)
    dataset = get_data(DATASET, dataset_parameters)
    dataset_grouped = get_data(DATASET_GROUPED, dataset_parameters)
    table = create_table(dataset, dataset_parameters)
    table_grouped = create_grouped_table(dataset_grouped, dataset_parameters)
    map = generate_map(dataset, dataset_parameters.attributes)
    return render_template(
        'index.html', 
        table=table, 
        table_grouped=table_grouped, 
        parameters=dataset_parameters, 
        map=map,
        order_by_options=order_by_options,
        search_options=search_options,
        order_options=order_options,
        sort_by_options=sort_by_options,
        shortcut_options=shortcut_options,
        checkbox_options=checkbox_options)

## RUN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)