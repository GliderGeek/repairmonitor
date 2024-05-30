import sqlite3
from pathlib import Path

from flask import Flask, render_template, g, request

app = Flask(__name__)

DATABASE = Path(__file__).parent / 'repairdata.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def index():
    brands = [row['brand'] for row in query_db('SELECT DISTINCT brand FROM repairs ORDER BY brand ASC ')]
    models = [row['model'] for row in query_db('SELECT DISTINCT model FROM repairs ORDER BY model ASC ')]
    product_kinds = [row['kind_of_product'] for row in query_db('SELECT DISTINCT kind_of_product FROM repairs ORDER BY kind_of_product ASC ')]
    return render_template('main.html', brands=brands, models=models, product_kinds=product_kinds)

@app.route('/repairs/')
def repairs():

    brand = request.args.get('brand')
    model = request.args.get('model')
    kind_of_product = request.args.get('kind')

    # todo: address sql injection vuln
    # todo: make such that brand is not required
    query = f"SELECT COUNT(*) FROM repairs WHERE brand='{brand}'"
    if model is not None:
        query += f" AND model='{model}'"
    if kind_of_product is not None:
        query += f" AND kind_of_product='{kind_of_product}'"

    res = query_db(query)
    number_of_results = (res[0]['COUNT(*)'])
    return {'number_of_results': number_of_results}
