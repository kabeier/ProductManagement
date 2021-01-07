from app import db
from .import bp as shop
from flask import render_template, redirect, url_for, request, flash, session, jsonify
from app.blueprints.authentication.models import User, UserRole
from flask_login import login_required, current_user
from datetime import datetime as dt
from .models import Product, Category


@shop.route('/create_category', methods=['GET', 'POST'])
@login_required
def create_category():
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.create:
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        try:
            form_data = request.form
            cat_name = form_data["category_name"].lower()
            newCat = Category()
            newCat.from_dict({"name": cat_name})
            newCat.save()
            flash('Category Added.', 'success')
            return redirect(url_for('shop.create_category'))
        except Exception:
            flash('There was a problem making your category. Please try again.', 'danger')
            return redirect(url_for('shop.create_category'))
    return render_template('shop/create_category.html')


@shop.route('/remove_category', methods=['GET', 'POST'])
@login_required
def remove_category():
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.delete:
        return redirect(url_for('main.index'))
    cats = Category.query.all()
    context = {
        "cats": cats
    }
    if request.method == 'POST':
        try:
            form_data = request.form
            print(form_data)
            cat = Category.query.filter_by(id=form_data["removeID"]).first()
            cat.remove()
            flash('Category Deleted.', 'success')
            return redirect(url_for('shop.remove_category'))
        except Exception:
            flash(
                'There was a problem deleting your category. Please try again.', 'danger')
            return redirect(url_for('shop.remove_category'))
    return render_template('shop/remove_category.html', **context)


@shop.route('/create_product', methods=['GET', 'POST'])
@login_required
def create_product():
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.create:
        return redirect(url_for('main.index'))
    cats = Category.query.all()
    context = {
        "cats": cats
    }
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            flash('Product Added.', 'success')
            product = Product()
            product.from_dict({
                'name': form_data['name'],
                'price': form_data['price'],
                'image': form_data['image'],
                'category_id': form_data['cat'],
                'tax': form_data['tax'],
                'description': form_data['desc']

            })
            print(product.to_dict)
            product.save()
            return redirect(url_for('shop.create_product'))
        except Exception:
            flash('There was a problem making your product. Please try again.', 'danger')
            return redirect(url_for('shop.create_product'))
    return render_template('shop/create_product.html', **context)


@shop.route('/remove_product', methods=['GET', 'POST'])
@login_required
def remove_product():
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.delete:
        return redirect(url_for('main.index'))
    prods = Product.query.all()
    context = {
        "prods": prods
    }
    if request.method == 'POST':
        try:
            form_data = request.form
            prod = Product.query.filter_by(id=form_data["removeID"]).first()
            prod.remove()
            flash('Product Deleted.', 'success')
            return redirect(url_for('shop.remove_product'))
        except Exception:
            flash(
                'There was a problem deleting your product. Please try again.', 'danger')
            return redirect(url_for('shop.remove_product'))
    return render_template('shop/remove_product.html', **context)


@shop.route('/edit_product', methods=['GET', 'POST'])
@login_required
def edit_product():
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.modify:
        return redirect(url_for('main.index'))
    prods = Product.query.all()
    context = {
        "prods": prods
    }
    if request.method == 'POST':
        form_data = request.form["selectID"]
        return redirect(url_for('shop.edit_product2', code=302, id=form_data))
    return render_template('shop/edit_product_select.html', **context)


@shop.route('/edit_product2', methods=['GET', 'POST'])
@login_required
def edit_product2():
    id = request.args.get("id", type=int)
    user = User.query.get(current_user.id)
    role = UserRole.query.filter_by(id=user.role_id).first()
    if not role.create:
        return redirect(url_for('main.index'))
    cats = Category.query.all()
    p = Product.query.filter_by(id=id).first()
    context = {
        "cats": cats,
        "p": p
    }
    if request.method == 'POST':
        try:
            form_data = request.form.to_dict()
            id = request.args.get("id", type=int)
            prod = Product.query.filter_by(id=id).first()
            prod.from_dict({
                'name': form_data['name'],
                'price': form_data['price'],
                'image': form_data['image'],
                'category_id': form_data['cat'],
                'tax': form_data['tax'],
                'description': form_data['desc']

            })
            prod.save()
            flash('Product edit successful.', 'success')
        except Exception:
            flash(
                'There was a problem editing your product. Please try again.', 'danger')
            return redirect(url_for('shop.edit_product'))
        return redirect(url_for('shop.edit_product'))
    return render_template('shop/edit_product.html', **context)
