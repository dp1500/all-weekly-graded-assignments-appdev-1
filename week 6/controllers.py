from flask import Flask, request, render_template
from flask import current_app as app
from models import *

@app.route('/',methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        students = Student.query.all()
        return render_template("index.html", students = students)