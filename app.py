import os

from flask import Flask, render_template, request, redirect, url_for

import repository.products as product_repository

app = Flask(__name__)

os.makedirs(app.instance_path, exist_ok=True)
product_repository.init_app(app.instance_path)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


def product_form(product, create):
    errors = []

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
        errors = product_repository.validate(product)

        if len(errors) == 0:
            product_repository.save(product)

            if create:
                return redirect(url_for("products_list"))

    name = request.args.get('name')

    if name is not None:
        products = product_repository.find_all_by_name(name)
    else:
        products = product_repository.find_all()

    return render_template(
        'products/list.html',
        create=create,
        default_product=product,
        errors=errors,
        products=products,
        name=name
    )


@app.route('/products', methods=("GET", "POST"))
def products_list():
    product = {
        'name': '',
        'unit_price': 0
    }

    return product_form(product, True)


@app.route('/products/create', methods=("GET", "POST"))
def products_create():
    product = {
        'name': '',
        'unit_price': 0
    }
    errors = []

    if request.method == "POST":
        product['name'] = request.form['name']
        product['unit_price'] = int(request.form['unit_price'])
        errors = product_repository.validate(product)

        if len(errors) == 0:
            product_repository.save(product)

            return redirect(url_for("products_list"))

    return render_template(
        'products/edit.html',
        product=product,
        errors=errors,
        create=True
    )


@app.route('/products/<int:product_id>/edit', methods=("GET", "POST"))
def products_edit(product_id):
    product = product_repository.find_one_by_id(product_id)

    return product_form(product, False)


@app.route('/products/<int:product_id>/delete', methods=["POST"])
def products_delete(product_id):
    product_repository.delete(product_id)
    return redirect(url_for("products_list"))


if __name__ == '__main__':
    app.run()
