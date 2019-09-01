from flask import Flask,render_template,request,Blueprint
from flask_ckeditor import CKEditor
import os
import pandas as pd


cq_app = Blueprint('Create_quiz',__name__)
#cq_app = Flask(__name__)
#ckeditor = CKEditor(cq_app)

i = 0
Class =0
Subject =""
Chapter = ""
No_of_questions = 0
Quiz_no = 0
dir = str(os.path.dirname(os.path.abspath(__name__))) + "/App/"
d_Que = pd.DataFrame()
d_Opt = pd.DataFrame()
d_Ans = pd.DataFrame()
d_Exp = pd.DataFrame()

def init():
    i = 0
    Class =0
    Subject =""
    Chapter = ""
    No_of_questions = 0
    Quiz_no = 0
    dir = str(os.path.dirname(os.path.abspath(__name__))) + "/App/"
    d_Que = pd.DataFrame()
    d_Opt = pd.DataFrame()
    d_Ans = pd.DataFrame()
    d_Exp = pd.DataFrame()

def preprocessing(question,options,answer,explanation):
    global d_Que,d_Opt,d_Ans,d_Exp
    option = ""

    if len(options) < 1:
        option = "__________#"
    else:
        for i in options.split('\r\n'):
            if len(i)>0:
                option += i[3:-4] + '#'
            option = option.replace('&nbsp;','')

    answer = answer.replace('<p>','')
    answer = answer.replace('</p>','')
    answer = answer.replace('&nbsp;','')
    answer = answer.replace('\r\n','')

    question = question.replace('<p>','')
    question = question.replace('</p>','')
    question = question.replace('&nbsp;','')
    question = question.replace('\r\n','')

    explanation = explanation.replace('<p>','')
    explanation = explanation.replace('</p>','')
    explanation = explanation.replace('&nbsp;','')
    explanation = explanation.replace('\r\n','')

    d_Que = d_Que.append(pd.DataFrame([question]))
    d_Opt = d_Opt.append(pd.DataFrame([option]))
    d_Ans = d_Ans.append(pd.DataFrame([answer]))
    d_Exp = d_Exp.append(pd.DataFrame([explanation]))

@cq_app.route('/admin/create')
def f():
    init()
    return render_template('Quiz/create/intro.html')

@cq_app.route('/admin/create_quiz', methods = ['GET','POST'])
def f1():
    global dir
    init()

    l = os.listdir(dir + 'dataset/quiz_data')
    global Class
    Class = "Class " + str(request.form['class'])
    if Class not in l:
        os.mkdir(dir + "dataset/quiz_data/" + str(Class))

    global Subject
    Subject = request.form['subject'].lower()
    l = os.listdir(dir + 'dataset/quiz_data/'+ Class)
    if Subject not in l:
        os.mkdir(dir + "dataset/quiz_data/" + Class + "/" + str(Subject))

    Chapter_name = request.form['Chapter_name'].lower()
    Chapter_no = request.form['chapter_number']
    global Chapter
    Chapter = str(Chapter_no) + ". " + str(Chapter_name[0].upper()) + str(Chapter_name[1:])

    l = os.listdir(dir + "dataset/quiz_data/" + Class + "/" + str(Subject))

    if Chapter not in l:
        os.mkdir(dir + "dataset/quiz_data/" + Class + "/" + str(Subject) + "/" + str(Chapter))

    global Quiz_no
    l = os.listdir(dir + "dataset/quiz_data/" + Class + "/" + str(Subject) + "/" + str(Chapter))
    Quiz_no = len(l) + 1

    global No_of_questions
    No_of_questions = int(request.form['No_of_questions'])

    global i
    i += 1
    return render_template('Quiz/create/index.html',No_of_questions = No_of_questions, Chapter_name = Chapter,i=i)

@cq_app.route('/admin/create_quiz_',methods = ['GET','POST'])
def f2():

    que = request.form.get('question')
    options = request.form.get('options')
    answer = request.form.get('answer')
    explanation = request.form.get('explanation')

    global Chapter
    global No_of_questions

    preprocessing(que,options,answer,explanation)

    global i
    i += 1
    return render_template('Quiz/create/index.html',No_of_questions = No_of_questions , Chapter_name = Chapter, i=i)

@cq_app.route('/admin/result',methods = ['GET','POST'])
def result():

    que = request.form.get('question')
    options = request.form.get('options')
    answer = request.form.get('answer')
    explanation = request.form.get('explanation')

    preprocessing(que,options,answer,explanation)

    global dQ,dO

    df = pd.concat([d_Que,d_Opt,d_Ans,d_Exp],axis=1)
    df.columns = ['Question','Options','Answer','Explanation']

    global Class,subject,Chapter,Quiz_no,dir
    df.to_csv(dir + "dataset/quiz_data/" + str(Class) + "/" + str(Subject) + "/" + str(Chapter) + "/" + str(Quiz_no) + ".csv",index=False)
    return render_template('Quiz/create/result.html', Chapter = Chapter[2:])
