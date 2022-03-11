# Suas rotas aqui
import csv
from http import HTTPStatus
from flask import Flask, jsonify, request
from app.products.csv_products import add_products_in_csv
from app.products.csv_products import rewrite_products_in_csv
from app.products.csv_products import format_values
from app.products.csv_products import read_all

import os

PATH = os.getenv("FILEPATH")

app = Flask(__name__)


@app.get("/products")
def home():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 3))

    products = read_all()

    products_paginator = products[(page*per_page)-per_page:page*per_page]

    new_list = []

    for product in products_paginator:
        format_values(product)
        new_list.append(product)

    return jsonify(new_list), HTTPStatus.OK


@app.get("/products/<product_id>")
def products(product_id):

    products = read_all()

    result = []

    for product in products:
        if product_id == product["id"]:
            result.append(product)

    if len(result) == 0:
        return {"message": "ID not found"}

    product_return = format_values(result[0])

    return product_return, HTTPStatus.OK


@app.post("/products")
def add_product():

    data = request.get_json()
    products = read_all()

    get_last_id = products[len(products) - 1]

    product_id = {"id": int(get_last_id["id"]) + 1}
    data.update(product_id)

    product_price = {"price": float(data["price"])}
    data.update(product_price)

    add_products_in_csv(data)

    return data, HTTPStatus.CREATED


@app.delete("/products/<product_id>")
def delete_product(product_id):

    product_id_int = int(product_id)
    products = read_all()

    new_products = [product for product in products if product["id"] != product_id]

    product_to_be_deleted = [product for product in products if product["id"] == product_id]

    rewrite_products_in_csv(new_products)

    product_return = format_values(product_to_be_deleted[0])
    print(product_return)

    message = "product id " + product_id + " not found"

    if len(product_to_be_deleted) == 0:
        return {"error": message}, HTTPStatus.NOT_FOUND

    return product_to_be_deleted[0], HTTPStatus.OK


@app.patch("/products/<product_id>")
def update_product(product_id):
    data = request.get_json()

    product_id_int = int(product_id)

    products = read_all()

    message = "product id " + product_id + " not found"

    product_to_be_changed = [product for product in products if product["id"] == product_id]

    new_list = []

    for product in products:
        if product["id"] == product_id:
            product["name"] = data["name"]
        new_list.append(product)

    product_return = format_values(product_to_be_changed[0])

    rewrite_products_in_csv(new_list)

    if len(product_to_be_changed) == 0:
        return {"error": message}, HTTPStatus.NOT_FOUND

    return (product_return), HTTPStatus.OK
