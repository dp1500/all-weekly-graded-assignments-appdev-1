from flask import Flask
from flask import render_template
from flask import request
import csv
import matplotlib.pyplot as plt

app = Flask(__name__)

listSids = []
listCids = []


with open("data.csv", 'r') as data:
    df = csv.reader(data)
    next(df)
    for line in df:
        listSids.append(line[0])
        listCids.append(line[1].split()[0])

def isValidSid(par):
    if par in listSids:
        return True
    else: return False

def isValidCid(par):
    if par in listCids:
        return True
    else: return False

def displayStudentData(studentid):
    content = []
    marks = 0
    with open("data.csv", 'r') as data:
        df = csv.reader(data)
        next(df)
        for line in df:
            if line[0] == studentid:
                content.append(line)
                marks += int(line[2])
    marks = str(marks)
    return render_template("displayStudent.html",listOfStudents = content, TotalMarks = marks)

def displayCourseData(courseId):
    with open("data.csv", 'r') as data:
        content = []
        total = 0
        max = 0
        count = 0

        df = csv.reader(data)
        next(df)
        for line in df:
            if line[1].split()[0] == courseId:
                content.append(line[2])

                total = total + int(line[2])
                count = count + 1
                
                if int(line[2]) > max:
                    max = int(line[2])
                
                
    avg = total/count
    

    # Creating histogram
    # fig, ax = plt.subplots(figsize =(10, 7))
    plt.hist(content)
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig('static/histogram.png')

    return render_template("displayCourse.html", avg = avg, max = max)


@app.route('/',methods = ["GET", "POST"])
def hello_world():
    if request.method == "GET":
        return render_template("index.html")

    elif request.method == "POST":
        id = request.form["ID"]
        idValue = request.form["id_value"]

        if id == "student_id" and isValidSid(idValue):
            return displayStudentData(idValue)
        
        elif id == "course_id" and isValidCid(idValue):
            return displayCourseData(idValue)
        
        else:
            return render_template("error.html")
    else:
        print("something went wring")

if __name__ == '__main__':
    app.debug = True
    app.run()