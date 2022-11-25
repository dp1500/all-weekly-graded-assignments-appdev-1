from flask_restful import Resource, fields, marshal_with,reqparse
from models import Course, Student, Enrollment
from database import db
from validation import *

# #defining json structure for marshal

# output_field = {
#   "course_id": 201,
#   "course_name": "Maths1",
#   "course_code": "MA101",
#   "course_description": "Course Description Example"
# }

Course_parser = reqparse.RequestParser()
Course_parser.add_argument('course_name')
Course_parser.add_argument('course_code')
Course_parser.add_argument('course_description')

class CourseApi(Resource):
    def get(self, courseId):
        
        course = db.session.query(Course).filter(Course.course_id == courseId).first()

        if course:
            return { "course_id": course.course_id, "course_name": course.course_name, "course_code": course.course_code, "course_description": course.course_description}
        else:
            return "Course not found", 404

    def put(self, courseId):  
        course = db.session.query(Course).filter(Course.course_id == courseId).first()
        if course:
            args =Course_parser.parse_args()
            course_name = args.get("course_name", None) 
            course_code = args.get("course_code", None)
            course_description = args.get("course_description", None)
            
            if (course_name is None) or (course_code is None):
                raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
        
            course.course_name = course_name
            course.course_code = course_code
            course.course_description = course_description

            db.session.commit()
            return { "course_id": course.course_id, "course_name": course.course_name, "course_code": course.course_code, "course_description": course.course_description}, 200

        else:
            return "course not found", 404
    
    def delete(self, courseId):
        course = db.session.query(Course).filter(Course.course_id == courseId).first()
        if course:
            db.session.delete(course)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            return "Course not found", 404
        # course = Course.query.get_or_404(courseId)

    def post(self):
        args =Course_parser.parse_args()
        course_name = args.get("course_name", None) 
        course_code = args.get("course_code", None)
        course_description = args.get("course_description", None)

        if course_name is None:
            raise BusinessValidationError(status_code= 400, error_code=	"COURSE001", error_message= "Course Name is required")
        if course_code is None:
            raise BusinessValidationError(status_code= 400, error_code=	"COURSE002", error_message= "Course Code is required")
        
        courseDuplicate = db.session.query(Course).filter(Course.course_code == course_code).first()
        if courseDuplicate:
            # raise BusinessValidationError(status_code= 409, error_code= "None",error_message= "course_code already exist")
            return "course_code already exists", 409
        
        new_course = Course(course_code = course_code,course_name= course_name,course_description = course_description)
        db.session.add(new_course)
        db.session.commit()
        
        return { "course_id": new_course.course_id, "course_name": new_course.course_name, "course_code": new_course.course_code, "course_description": new_course.course_description}, 201
        # "Successfully Created",



student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name')
student_parser.add_argument('last_name')
student_parser.add_argument('roll_number')

class StudentApi(Resource):
    def get(self, studentId):
        student = db.session.query(Student).filter(Student.student_id == studentId).first()
        if student:
            return { "student_id": student.student_id , "first_name": student.first_name, "last_name": student.last_name , "roll Number": student.roll_number}, 200
        
        else:
            return "Student not found",404
    
    def post(self):
        args =student_parser.parse_args()
        first_name = args.get("first_name", None) 
        last_name = args.get("last_name", None)
        roll_number = args.get("roll_number", None)

        if first_name is None:
            raise BusinessValidationError(status_code= 400, error_code=	"STUDENT002", error_message= "First Name is required")
            
        if roll_number is None:
            raise BusinessValidationError(status_code= 400, error_code=	"STUDENT001", error_message= "Roll Number required")
            # return { "error_code": "string","error_message": "string"}
        
        courseDuplicate = db.session.query(Student).filter(Student.roll_number == roll_number).first()
        if courseDuplicate:
            # raise BusinessValidationError(status_code= 409, error_code= "None",error_message= "course_code already exist")
            return "Student already exists", 409

        new_student = Student(first_name = first_name, last_name= last_name, roll_number = roll_number)
        db.session.add(new_student)
        db.session.commit()
        
        return { "student_id": new_student.student_id , "first_name": new_student.first_name, "last_name": new_student.last_name , "roll Number": new_student.roll_number}, 201


    def put(self, studentId):
        student = db.session.query(Student).filter(Student.student_id == studentId).first()
        if student:
            args =student_parser.parse_args()
            first_name = args.get("first_name", None) 
            last_name = args.get("last_name", None)
            roll_number = args.get("roll_number", None)
            
            if (roll_number is None) or (first_name is None):
                raise BusinessValidationError(status_code= 400, error_code=	"string", error_message= "string")
        
            student.first_name = first_name
            student.last_name = last_name
            student.roll_number = roll_number

            db.session.commit()
            return { "student_id": student.student_id , "first_name": student.first_name, "last_name": student.last_name , "roll Number": student.roll_number}, 200
        
        else:
            return "student not found", 404

    def delete(self, studentId):
        stduent = db.session.query(Student).filter(Student.student_id == studentId).first()
        if stduent:
            db.session.delete(stduent)
            db.session.commit()
            return "Successfully Deleted", 200
        else:
            return "student not found", 404




enroll_parser = reqparse.RequestParser()
enroll_parser.add_argument("course_id")
 
# class EnrollementsApi(Resource):
#     def get(self, studentId):
#         student = db.session.query(Student).filter(Student.student_id == studentId).first()
#         if student:
#             enrollments = Enrollment.query.filter(Enrollment.student_id == studentId).all()
#             if enrollments == []:
#                 raise NotFoundError(status_code=404)

#             list_of_enrolls = []

#             for enroll in enrollments:
#                 output = {
#                         "enrollment_id": enroll.enrollment_id,
#                         "student_id": enroll.estudent_id,
#                         "course_id": enroll.ecourse_id
#                     }
#                 list_of_enrolls.append(output)

#                 return list_of_enrolls, 200
#         else:
#             raise BusinessValidationError(status_code= 400, error_code=	"ENROLLMENT002", error_message= "Student does not exist.")
            
            
    
#     def post(self,studentId):
#         args =enrollement_parser.parse_args()
#         courseID = args.get("courseID", None) 
        
#         student = db.session.query(Student).filter(Student.student_id == studentId).first()
#         if student:
#             # print(courseID)
#             course = db.session.query(Course).filter(Course.course_id == courseID).first()
#             if course:
#                 new_enrollement = Enrollment(estudent_id = studentId, ecourse_id = courseID)
#                 db.session.add(new_enrollement)
#                 db.session.commit()

#                 enrollments = Enrollment.query.filter(Enrollment.student_id == studentId).all()
#                 if enrollments == []:
#                     raise NotFoundError(status_code=404)

#                 list_of_enrolls = []

#                 for enroll in enrollments:
#                     output = {
#                         "enrollment_id": enroll.enrollment_id,
#                         "student_id": enroll.estudent_id,
#                         "course_id": enroll.ecourse_id
#                     }
#                     list_of_enrolls.append(output)

#                 return list_of_enrolls, 201


#             else:
#                 raise BusinessValidationError(status_code= 400, error_code=	"ENROLLMENT001", error_message= "Course does not exist.")
            
#         else:
#             raise BusinessValidationError(status_code= 400, error_code=	"ENROLLMENT002", error_message= "Student does not exist.")
            
#     def delete(self, studentId,courseId):
#         student = db.session.query(Student).filter(Student.student_id == studentId).first()
#         if student == None:
#             raise BusinessValidationError(status_code= 400, error_code=	"ENROLLMENT002", error_message= "Student does not exist.")

#         course = db.session.query(Course).filter(Course.course_id == courseId).first()
#         if course ==None:
#             raise BusinessValidationError(status_code= 400, error_code=	"ENROLLMENT001", error_message= "Course does not exist.")
            

#         enrollements = db.session.query(Enrollment).filter((Enrollment.estudent_id == studentId) & (Enrollment.ecourse_id == courseId)).first()
        
#         if enrollements == []:
#             raise NotFoundError(status_code=404)

#         for enrollement in enrollements: 
#             db.session.delete(enrollement)
#         db.session.commit()

#         return "Successfully Deleted", 200
        
class EnrollmentAPI(Resource):
    def get(self, student_id):
        student = Student.query.filter(Student.student_id == student_id).scalar()

        if student is None:
            raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")
        enrollements = Enrollment.query.filter(Enrollment.student_id == student_id).all()

        if enrollements == []:
            raise NotFoundError(status_code=404)

        list_of_enrollements = []

        for enroll in enrollements:
            msg = {
                "enrollment_id": enroll.enrollment_id,
                "student_id": enroll.student_id,
                "course_id": enroll.course_id
            }
            list_of_enrollements.append(msg)

        return list_of_enrollements, 200

    def post(self, student_id):
        args = enroll_parser.parse_args()
        course_id = args.get("course_id", None)

        student = Student.query.filter(Student.student_id == student_id).scalar()

        if student is None:
            raise BusinessValidationError(status_code=400,error_code="ENROLLMENT002",error_message="Student does not exist")

        course = Course.query.filter(Course.course_id == course_id).scalar()

        if course is None:
            raise BusinessValidationError(status_code=400,error_code="ENROLLMENT001",error_message="Course does not exist"
            )

        enroll = Enrollment(
            student_id=student_id,
            course_id=course_id
        )

        db.session.add(enroll)
        db.session.commit()

        enrolls = Enrollment.query.filter(
            Enrollment.student_id == student_id).all()

        if enrolls == []:
            raise NotFoundError(status_code=404)

        list_of_enrollements = []

        for enroll in enrolls:
            msg = {
                "enrollment_id": enroll.enrollment_id,
                "student_id": enroll.student_id,
                "course_id": enroll.course_id
            }
            list_of_enrollements.append(msg)

        return list_of_enrollements, 201

    def delete(self, course_id, student_id):
        student = Student.query.filter(
            Student.student_id == student_id).scalar()

        if student is None:
            raise BusinessValidationError(
                status_code=400,
                error_code="ENROLLMENT002",
                error_message="Student does not exist"
            )

        course = Course.query.filter(Course.course_id == course_id).scalar()

        if course is None:
            raise BusinessValidationError(
                status_code=400,
                error_code="ENROLLMENT001",
                error_message="Course does not exist"
            )

        enrolls = Enrollment.query.filter(
            Enrollment.student_id == student_id and Enrollment.course_id == course_id
        ).all()

        if enrolls == []:
            raise NotFoundError(status_code=404)

        for enroll in enrolls:
            db.session.delete(enroll)
        db.session.commit()

        return "", 200      