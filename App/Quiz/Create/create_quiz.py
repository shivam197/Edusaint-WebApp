from flask import Flask,render_template,request,Blueprint
from flask_ckeditor import CKEditor
import os
import pandas as pd


cq_app = Blueprint('Create_quiz',__name__)
#cq_app = Flask(__name__)
#ckeditor = CKEditor(cq_app)

i = 0
Class = 0
Subject = ""
Chapter = ""
No_of_questions = 0
Quiz_no = 0
directory = os.path.join((os.path.dirname(os.path.abspath(__name__))),"App")
d_Que = pd.DataFrame()
d_Opt = pd.DataFrame()
d_Ans = pd.DataFrame()
d_Exp = pd.DataFrame()

def init():
    global i,Class,Subject,Chapter,No_of_questions,Quiz_no,directory,d_Exp,d_Opt,d_Que,d_Ans
    i = 0
    Class =0
    Subject =""
    Chapter = ""
    No_of_questions = 0
    Quiz_no = 0
    directory = os.path.join((os.path.dirname(os.path.abspath(__name__))),"App")
    d_Que = pd.DataFrame()
    d_Opt = pd.DataFrame()
    d_Ans = pd.DataFrame()
    d_Exp = pd.DataFrame()

def delete():
    global i,Class,Subject,Chapter,No_of_questions,Quiz_no,d_Que,directory,d_Opt,d_Ans, d_Exp
    del i
    del Class
    del Subject
    del Chapter
    del No_of_questions
    del Quiz_no
    del d_Que
    del directory
    del d_Opt
    del d_Ans
    del d_Exp

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
        #All options are stored as a single sentence seperated by '#'

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
def create_quiz_intro_function():
    init()
    return render_template('Quiz/create/intro.html')

@cq_app.route('/admin/create_quiz', methods = ['GET','POST'])
def create_quiz_function1():
    global directory
    init()
    l = os.listdir(os.path.join(directory,'dataset'))
    directory = os.path.join(directory,'dataset','quiz_data')
    if len(l) == 0:
        os.mkdir(directory)

    global Class
    Class = "Class " + str(request.form['class'])
    l = os.listdir(directory)
    directory = os.path.join(directory,Class)
    if Class not in l:
        os.mkdir(directory)

    global Subject
    Subject = request.form['subject'].lower()
    l = os.listdir(directory)
    directory = os.path.join(directory,Subject)
    if Subject not in l:
        os.mkdir(directory)

    Chapter_name = request.form['Chapter_name'].lower()
    Chapter_no = request.form['chapter_number']
    global Chapter
    Chapter = str(Chapter_no) + ". " + str(Chapter_name[0].upper()) + str(Chapter_name[1:])

    l = os.listdir(directory)
    directory = os.path.join(directory,Chapter)
    if Chapter not in l:
        os.mkdir(directory)

    global Quiz_no
    l = os.listdir(directory)
    Quiz_no = len(l) + 1
    directory = os.path.join(directory,(str(Quiz_no) + ".csv"))
    global No_of_questions
    No_of_questions = int(request.form['No_of_questions'])

    global i
    i += 1
    return render_template('Quiz/create/index.html',No_of_questions = No_of_questions, Chapter_name = Chapter,i=i)

@cq_app.route('/admin/create_quiz_',methods = ['GET','POST'])
def create_quiz_function2():

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
def create_quiz_result():
    que = request.form.get('question')
    options = request.form.get('options')
    answer = request.form.get('answer')
    explanation = request.form.get('explanation')

    preprocessing(que,options,answer,explanation)

    global d_Que,d_Opt,d_Ans,d_Exp

    df = pd.concat([d_Que,d_Opt,d_Ans,d_Exp],axis=1)
    df.columns = ['Question','Options','Answer','Explanation']

    global Class,subject,Chapter,Quiz_no,directory
    df.to_csv(directory,index=False)
    Chap = Chapter[2:]
    del df
    delete()
    return render_template('Quiz/create/result.html', Chapter = Chap)
