# -*- coding: utf-8 -*-
# from app import app
from flask import render_template, Flask, url_for, session, request
from config import basedir
from . import blueprint
from app import babel
# from config import LANGUAGES
# from config import LOCALES
    
@blueprint.route('/')
@blueprint.route('/index')
def index():
    f = open(basedir+"/app/static/index_nutri.re", "r")
    text =  f.read()
    f.close()
    return render_template('index.html', text = text)

@blueprint.route('/pruebas')
def pruebas():
    return render_template('pruebas.html')




@babel.localeselector
def get_locale():
    # return "es" #request.accept_languages.best_match(LANGUAGES.keys())
    # print "locales:", LOCALES
    # print "languajes:",LANGUAGES.keys()
    # print request.accept_languages.best_match(LANGUAGES.keys()),"/n"
    # print request.accept_languages.best_match(LOCALES)
    return "es"#request.accept_languages.best_match(LANGUAGES.keys())


