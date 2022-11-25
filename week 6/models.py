from database import db

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    course_code = db.Column(db.String, unique = True, nullable = False)
    course_name = db.Column(db.String, nullable = False)
    course_description = db.Column(db.String)

    def _init_(self, course_code, course_name, course_description):
        self.course_code = course_code
        self.course_name = course_name
        self.course_description = course_description
        
        

class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    roll_number = db.Column(db.String, unique = True, nullable = False)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String)

    def _init_(self, roll, f_name, l_name):
        self.roll_number = roll
        self.first_name = f_name
        self.last_name = l_name

class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.student_id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

    # def _init_(self, es_id, ec_id):
    #     self.estudent_id = es_id
    #     self.ecourse_id = ec_id