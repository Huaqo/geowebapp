import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from tabulate import tabulate
from sqlalchemy import text
from models import db
from queries import HOCHSCHULEN
from flask import request

def get_hochschulen_data(order, limit, sort_by, attributes, search, search_attr):
    attributes = [attr for attr in attributes if attr]
    query = text(HOCHSCHULEN.format(order=order, limit=limit, sort_by=sort_by, attributes=', '.join(attributes), search_attr=search_attr))
    result = db.session.execute(query, {'search': f'%{search}%'})
    hochschulen = result.fetchall()
    return hochschulen

def create_hochschulen_table(order, limit, sort_by, attributes, search, search_attr):
    attributes = [attr for attr in attributes if attr]
    hochschulen = get_hochschulen_data(order, limit, sort_by, attributes, search, search_attr)
    table_data = [list(row) for row in hochschulen]
    table = tabulate(table_data, headers=attributes, tablefmt='html')
    return table

# Fallback variables
default_order = 'ASC'
default_limit = '10'
default_sort_by = 'gjahr'
default_attributes = ['name_h']
default_search_attr = 'name_h'

def get_form_parameters():
    order = request.args.get('order', default_order)
    limit = request.args.get('limit', default_limit)
    sort_by = request.args.get('sort_by', default_sort_by)
    attributes = request.args.getlist('attributes')
    if not attributes:
        attributes = default_attributes
    search = request.args.get('search', '')
    search_attr = request.args.get('search_attr', default_search_attr)
    return order, limit, sort_by, attributes, search, search_attr
