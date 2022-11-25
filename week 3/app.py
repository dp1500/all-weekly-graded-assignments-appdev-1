import csv
import sys
import matplotlib
import matplotlib.pyplot as plt
from jinja2 import Template



# para1 = str(input("enmter pararar 1"))
# para2 = str(input("enter para 2"))

para1 = str(sys.argv[1])
para2 = str(sys.argv[2])

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


if para1 == "-s" and isValidSid(para2):
    content = []
    marks = 0
    with open("data.csv", 'r') as data:
        df = csv.reader(data)
        next(df)
        for line in df:
            if line[0] == para2:
                content.append(line)
                marks += int(line[2])
    marks = str(marks)
        
    temp = Template("""<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>Student Data</title>
                        </head>

                        <body>
                            <h1> Student Details  </h1>

                            <table border = 1px>
                                <thead>
                                    <tr>
                                        <th>Student id</th>
                                        <th>Course id</th>
                                        <th>Marks</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for line in content %}
                                    <tr>
                                        <td>{{line[0]}}</td>
                                        <td>{{line[1]}}</td>
                                        <td>{{line[2]}}</td>
                                    </tr>
                                    {% endfor %}
                                    <tr>
                                        <td colspan="2" align ="center">Total Marks</td>
                                        <td>{{marks}}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </body>""")
    out = temp.render(content = content, marks = marks)
    output = open('output.html', 'w')
    output.write(out)
    output.close()


elif para1 == "-c" and isValidCid(para2):
    content = []
    total = 0
    max = 0
    count = 0
    with open("data.csv", 'r') as data:

        df = csv.reader(data)
        next(df)
        for line in df:

            if line[1].split()[0] == para2:

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
    plt.savefig('histogram.png')

    temp = Template("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Course Data</title>
            </head>
            <body>
                <h1>Course Details</h1>

                <table border = 1px>
                    <tr>
                        <td >Average Marks</td>
                        <td>Maximum Marks</td>
                    </tr>
                    <tr>
                        <td>{{avg}}</td>
                        <td>{{max}}</td>
                    </tr>
                </table>
            
            <img src = "histogram.png">

            </body>
            </html>""")

    out = temp.render(avg = avg, max = max)
    output = open('output.html', 'w')
    output.write(out)
    output.close()

    
    

else:
    temp = Template("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Something Went Wrong</title>
            </head>
            <body>
                <h1>
                    Wrong Inputs
                </h1>
                <h4>
                    Something went wrong
                </h4>
            </body>
            </html>""")
    out = temp.render()
    output = open('output.html', 'w')
    output.write(out)
    output.close()    
    


# with open("data.csv", 'r') as data:
#     df = csv.reader(data)

# temp = Template()

