from csv import DictReader, DictWriter
import csv
import os

PATH = os.getenv("FILEPATH")


def read_products_from_csv():
    with open(PATH, "r") as csv_file:

        reader = DictReader(csv_file)
        products = list(reader)

        for product in products:
            for item in product:
                if item == "price":
                    new_price = {"price": float(product["price"])}
                    product.update(new_price)
                elif item == "id":
                    new_id = {"id": int(product["id"])}
                    product.update(new_id)

        return products


def add_products_in_csv(payload: dict):
    with open(PATH, "a") as csv_file:
        fieldnames = ["id", "name", "price"]
        writer = DictWriter(csv_file, fieldnames)

        writer.writerow(payload)


def rewrite_products_in_csv(payload: list[dict]):
    with open(PATH, "w") as csv_file:
        fieldnames = ["id", "name", "price"]
        writer = DictWriter(csv_file, fieldnames)

        writer.writeheader()
        writer.writerows(payload)


def format_values(product: dict):
    for item in product:
        if item == "price":
            new_price = {"price": float(product["price"])}
            product.update(new_price)
        elif item == "id":
            new_id = {"id": int(product["id"])}
            product.update(new_id)

    return product


def read_all():
    file = open(PATH, "r")
    file_read = csv.DictReader(file)
    products_in_csv = [product for product in file_read]
    file.close()
    return products_in_csv
