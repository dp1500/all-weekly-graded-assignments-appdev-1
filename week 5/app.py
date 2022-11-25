from flask import Flask, url_for, redirect
from flask import render_template
from flask import request
import os
import matplotlib.pyplot as plt

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, ForeignKey, delete

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir ,"database.sqlite3" )
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Course(db.Model):
    _tablename_ = 'course'
    course_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String, nullable = False)
    course_description = db.Column(db.String)

class Student(db.Model):
    _tablename_ = 'student'
    student_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)

    def _init_(self, roll, f_name, l_name):
        self.roll_number = roll
        self.first_name = f_name
        self.last_name = l_name

class Enrollments(db.Model):
    _tablename_ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), primary_key = True, nullable = False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), primary_key = True, nullable = False)

    def _init_(self, es_id, ec_id):
        self.estudent_id = es_id
        self.ecourse_id = ec_id

def getCourseId(name):
    if name == "course_1":
        return 1
    if name == "course_2":
        return 2
    if name == "course_3":
        return 3
    if name == "course_4":
        return 4

engine = create_engine("sqlite:///./database.sqlite3")




@app.route('/',methods = ["GET", "POST"])
def home():
    if request.method == "GET":
        students = Student.query.all()
        return render_template("index.html", students = students )

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == "GET":
        return render_template("create.html")
    elif request.method == "POST":
        
        rollNo = request.form['roll']
        fname = request.form['f_name']
        lname = request.form['l_name']

        

        newStud = Student(roll_number = rollNo, first_name = fname, last_name=lname)

        try:
            if bool(Student.query.filter_by(roll_number = newStud.roll_number).first()) == False:
                db.session.add(newStud)
                
                for i in range(len(request.form.getlist('courses'))):
                    obj = db.session.query(Student).order_by(Student.student_id.desc()).first()

                    newEnroll = Enrollments(estudent_id = obj.student_id, ecourse_id = getCourseId(request.form.getlist('courses')[i]))
                    db.session.add(newEnroll)
                    
                    

                db.session.commit()
                return redirect('/')
            else:
                return render_template("exists.html")
        except:
            return 'There was an issue adding student'
    else:
        pass

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update(student_id):
    if request.method == "GET":
        student = Student.query.get_or_404(student_id)
        return render_template("update.html",Student = student)

    if  request.method == "POST":
        
        fname = request.form['f_name']
        lname = request.form['l_name'] 

        try:
            # if bool(Student.query.filter_by(roll_number = newStud.roll_number).first()) == False:
            student = Student.query.get_or_404(student_id)
            student.first_name = fname
            student.last_name = lname

            Enrollments.query.filter_by(estudent_id = student_id).delete()
            
            estudentID = student_id
            Enrollments.query.filter_by(estudent_id = estudentID).delete()

            db.session.commit()

            for i in range(len(request.form.getlist('courses'))):
                obj = db.session.query(Student).order_by(Student.student_id.desc()).first()

                newEnroll = Enrollments(estudent_id = obj.student_id, ecourse_id = getCourseId(request.form.getlist('courses')[i]))
                db.session.add(newEnroll)
                    
            db.session.commit()
            return redirect('/')
            
        except:
            return 'There was an issue adding student'

@app.route('/student/<int:student_id>/delete', methods=['GET', 'POST'])
def delete(student_id):
    if request.method == "GET":
        task_to_delete1 = Student.query.get_or_404(student_id)
        estudentID = student_id
        print(type(estudentID))
        

        try:
            db.session.delete(task_to_delete1)
            Enrollments.query.filter_by(estudent_id = estudentID).delete()
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem deleting that task'

@app.route('/student/<int:student_id>', methods=['GET', 'POST'])
def details(student_id):
    if request.method == "GET":
        student = Student.query.get_or_404(student_id)
        estudentID = student_id
        
        # use join yaha

        enrols = Enrollments.query.filter_by(estudent_id = estudentID).all()

        Courses = db.session.query(Course).join(Enrollments).filter(Enrollments.estudent_id == estudentID).all()

        # Courses = Course.query.filter_by(course_id = enrols.ecourse_id)
        return render_template("details.html",student = student, Courses = Courses)
    
if __name__ == '__main__':
    app.debug = True
    app.run()