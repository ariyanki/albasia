from app import app
from flask import render_template, request, redirect, url_for, session, flash, json

class Main():
    def __init__(self):

        @app.route('/main', methods=['GET','POST'])
        def main():
            return render_template('/main/main.html')

        @app.route("/")
        def home():
            return render_template('/main/index.html')

