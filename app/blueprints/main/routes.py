from flask import render_template, request, redirect, url_for, flash
from .import bp as main
from flask_login import login_required, current_user

@main.route('/', methods=['GET'])
@login_required
def index():

    return render_template('main/index.html')
