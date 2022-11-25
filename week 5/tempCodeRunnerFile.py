delete =  Enrollments.query.flter_by(estudent_id = student.student_id).all()
            # db.session.delete(delete)