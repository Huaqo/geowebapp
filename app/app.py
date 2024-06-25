from flask import render_template
from models import db
from init import create_app
from logic import get_data, create_table, get_parameters
from queries import HOCHSCHULEN

app = create_app()

@app.route('/', methods=['GET'])
def home():
    parameters = get_parameters()
    hochschulen = get_data(HOCHSCHULEN, parameters)
    table = create_table(hochschulen, parameters)
    return render_template('index.html', table=table, parameters=parameters)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)