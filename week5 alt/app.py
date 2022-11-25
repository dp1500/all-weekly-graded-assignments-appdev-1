import flask
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request


'''basedir = os.path.abspath(os.path.dirname(__file__))'''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
'''app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "database.sqlite3")'''
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()




class student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number= db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)


class course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)


class enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'GET':
        students = student.query.all()
        return render_template("index.html",students = students)


@app.route('/student/create', methods=['GET', 'POST'])
def addStudent():
    if request.method == 'GET':
        return render_template('addstudent.html')
    elif request.method == 'POST':
        try:
            roll_number = request.form['roll']
            first_name = request.form['f_name']
            last_name = request.form['l_name']
            Stu = student(roll_number=roll_number,
                              first_name=first_name, last_name=last_name)
            db.session.add(Stu)
            db.session.flush()
            courses = request.form.getlist('courses')
            for course in courses:
                
                enroll = enrollments(estudent_id=Stu.student_id, ecourse_id=int(course[-1]))
                db.session.add(enroll)
        except:
            db.session.rollback()
            return render_template('error.html')
        else:
            db.session.commit()
            return flask.redirect('/')


@app.route('/student/<stud_id>/update', methods=['GET', 'POST'])
def update(stud_id):
    if request.method == 'GET':
        Stu = student.query.get(stud_id)
        return render_template('update.html', student=Stu)

    elif request.method == 'POST':
        first_name = request.form['f_name']
        
        last_name = request.form['l_name']
        
        Stu = student.query.get(stud_id)
        Stu.first_name = first_name
        Stu.last_name = last_name
        

        enrollments.query.filter_by(estudent_id=stud_id).delete()
        db.session.flush()
        courses = request.form.getlist('courses')
        for course in courses:
            enroll = enrollments(estudent_id=stud_id,
                                 ecourse_id=int(course[-1]))
            db.session.add(enroll)

        db.session.commit()
        return flask.redirect('/')


@app.route('/student/<stud_id>/delete', methods=['GET', 'POST'])
def delete(stud_id):
        Stu = student.query.filter_by(student_id=stud_id).delete()
        enrollments.query.filter_by(estudent_id=stud_id).delete()
        db.session.flush()
        db.session.commit()
        return flask.redirect('/')
    

@app.route('/student/<stud_id>', methods=['GET', 'POST'])
def student_details(stud_id):
    Stu_list = student.query.get(stud_id)
    enroll_list = enrollments.query.filter_by(estudent_id=stud_id).with_entities(enrollments.ecourse_id)
    lst = []
    for num in enroll_list:
        lst.append(num['ecourse_id'])
    
    c_list = course.query.join(enrollments, enrollments.ecourse_id == course.course_id).filter_by(estudent_id=stud_id).with_entities(course.course_code, course.course_name,course.course_description)
   
    return render_template('studentdetails.html', student=Stu_list,courses=c_list)



if __name__ == "__main__":
    app.run()

