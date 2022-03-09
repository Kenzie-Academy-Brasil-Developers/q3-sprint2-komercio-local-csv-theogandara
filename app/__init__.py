# Suas rotas aqui
from http import HTTPStatus
from flask import Flask, jsonify, request
from app.products.csv_products import read_products_from_csv
from app.products.csv_products import add_products_in_csv
from app.products.csv_products import rewrite_products_in_csv

app = Flask(__name__)


@app.get("/products")
def home():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 3))

    products = read_products_from_csv()

    products_paginator = products[(page*per_page)-per_page:page*per_page]
    return jsonify(products_paginator), HTTPStatus.OK


@app.get("/products/<product_id>")
def products(product_id):

    products = read_products_from_csv()

    result = []

    for product in products:
        if int(product_id) == product["id"]:
            result.append(product)

    if len(result) == 0:
        return {"message": "ID not found"}

    return result[0], HTTPStatus.OK


@app.post("/products")
def add_product():

    data = request.get_json()
    products = read_products_from_csv()

    get_last_id = products[len(products) - 1]

    product_id = {"id": int(get_last_id["id"]) + 1}
    data.update(product_id)

    product_price = {"price": float(data["price"])}
    data.update(product_price)

    add_products_in_csv(data)

    return data, HTTPStatus.CREATED


@app.delete("/products/<product_id>")
def delete_product(product_id):

    product_id = int(product_id)
    product_id_print = str(product_id)
    products = read_products_from_csv()

    product_to_be_deleted = [product for product in products if product["id"] == product_id]

    new_list = [product for product in products if product["id"] != product_id]

    message = "product id " + product_id_print + " not found"

    rewrite_products_in_csv(new_list)

    if len(product_to_be_deleted) == 0:
        return {"error": message}, HTTPStatus.NOT_FOUND

    return product_to_be_deleted[0], HTTPStatus.OK


@app.patch("/products/<product_id>")
def update_product(product_id):
    data = request.get_json()

    product_price = {"price": float(data["price"])}
    data.update(product_price)

    product_id = int(product_id)
    product_id_print = str(product_id)

    products = read_products_from_csv()
    message = "product id " + product_id_print + " not found"

    product_to_be_changed = []

    for product in products:
        if product_id == product["id"]:
            product_to_be_changed.append(product)

    if len(product_to_be_changed) == 0:
        return {"error": message}, HTTPStatus.NOT_FOUND

    product_to_be_changed[0].update(data)
    return (product_to_be_changed[0]), HTTPStatus.OK
