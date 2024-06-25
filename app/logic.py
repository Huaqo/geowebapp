# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
# import io
from tabulate import tabulate
from sqlalchemy import text
from models import db
from queries import HOCHSCHULEN
from flask import request

class Parameters:
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

def get_parameters():
    parameters = Parameters()
    parameters.update(
        order=request.args.get('order', parameters.order),
        limit=request.args.get('limit', parameters.limit),
        sort_by=request.args.get('sort_by', parameters.sort_by),
        attributes=request.args.getlist('attributes') or parameters.attributes,
        search=request.args.get('search', parameters.search),
        search_attr=request.args.get('search_attr', parameters.search_attr)
    )
    parameters.attributes = [attr for attr in parameters.attributes if attr]
    return parameters

def get_data(query_template, parameters):
    params_dict = {k: v for k, v in parameters.__dict__.items()}
    for key, value in params_dict.items():
        if isinstance(value, list):
            params_dict[key] = ', '.join(value)
    query = query_template.format(**params_dict)  
    result = db.session.execute(text(query), {'search': f"%{params_dict.get('search', '')}%"})
    return result.fetchall()

def create_table(data, parameters):
    table_data = [list(row) for row in data]
    table = tabulate(table_data, headers=parameters.attributes, tablefmt='html')
    return table