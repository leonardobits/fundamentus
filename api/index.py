#!/usr/bin/env python3

from flask import Flask, jsonify
from fundamentus_stocks import get_data as get_stocks_data
from fundamentus_fii import get_data as get_fii_data
from datetime import datetime

app = Flask(__name__)

# First update
stocks, fii = dict(get_stocks_data()), dict(get_fii_data())
dia = datetime.strftime(datetime.today(), '%d')
stocks = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in stocks.items()}
fii = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in fii.items()}

@app.route("/")
def json_api_stocks():
    global stocks, dia
    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
        return jsonify(stocks)
    else:
        stocks, dia = dict(get_stocks_data()), datetime.strftime(datetime.today(), '%d')
        stocks = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in stocks.items()}
        return jsonify(stocks)

@app.route("/fii")
def json_api_fii():
    global fii, dia
    
    # Then only update once a day
    if dia == datetime.strftime(datetime.today(), '%d'):
        return jsonify(fii)
    else:
        fii, dia = dict(get_fii_data()), datetime.strftime(datetime.today(), '%d')
        fii = {outer_k: {inner_k: float(inner_v) for inner_k, inner_v in outer_v.items()} for outer_k, outer_v in fii.items()}
        return jsonify(fii)

app.run(debug=True)
