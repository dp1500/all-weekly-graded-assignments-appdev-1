from flask_restful import Resource, Api
import os 
from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))

## configuring app and api initialisation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "api_database.sqlite3") 
from database import db
db.init_app(app)
api = Api(app)
api.init_app(app)
app.app_context().push()

from apii import CourseApi,StudentApi, EnrollmentAPI

api.add_resource(StudentApi, "/api/student", "/api/student/<int:studentId>")
api.add_resource(CourseApi, "/api/course","/api/course/<int:courseId>")
api.add_resource(EnrollmentAPI, "/api/student/<int:student_id>/course", "/api/student/<int:student_id>/course/<int:course_id>")      

if __name__ == '__main__':
  # Run the Flask app
  app.run(
    host='0.0.0.0',
    debug=True,
    port=8080
  )

