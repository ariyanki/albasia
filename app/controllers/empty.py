from app import app
from flask import render_template, request, redirect, url_for, session, flash, json

class Empty():
    def __init__(self):

        @app.route("/")
        def empty():
            return render_template('/empty/index.html')

