# coding=utf-8
import pymssql
from flask import Flask, Response, render_template, request, redirect, jsonify

from Prepare import Prepare

app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/detail', methods=["get"])
def detail():
    return render_template('detail.html')


@app.route('/search', methods=["GET"])
def search():
    bt = request.args.get('begintime')
    et = request.args.get('endtime')
    # request.form.get('endtime') post获取参数的方式
    name = request.args.get('apiname')  # get获取参数的方式
    p = Prepare(bt, et, name)
    p.sql_sentence()
    p.create_qushitu()
    with open('qushi.png', 'rb') as f:
        return Response(f.read(), mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
