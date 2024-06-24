from flask import render_template, request
from models import db
from init import create_app
from logic import create_hochschulen_table, get_form_parameters

app = create_app()

@app.route('/', methods=['GET'])
def home():
    order, limit, sort_by, attributes, search, search_attr = get_form_parameters()
    table = create_hochschulen_table(order, limit, sort_by, attributes, search, search_attr)
    return render_template('index.html', table=table, order=order, limit=limit, sort_by=sort_by, attributes=attributes, search=search, search_attr=search_attr)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)