from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from flask_ckeditor import CKEditor
import os
import pandas as pd


app = Flask(__name__)
ckeditor = CKEditor(app)

i = 0

Class =0
Subject =""
Chapter = ""
No_of_questions = 0
Quiz_no = 0

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

@app.route('/')
def f():
    #initialize()
    return render_template('create_quiz/intro.html')

@app.route('/f1', methods = ['GET','POST'])
def f1():
    l = os.listdir('dataset/quiz_data')
    global Class
    Class = "Class " + str(request.form['class'])
    if Class not in l:
        os.mkdir("dataset/quiz_data/" + str(Class))

    global Subject
    Subject = request.form['subject'].lower()
    l = os.listdir('dataset/quiz_data/'+ Class)
    if Subject not in l:
        os.mkdir("dataset/quiz_data/" + Class + "/" + str(Subject))

    Chapter_name = request.form['Chapter_name'].lower()
    Chapter_no = request.form['chapter_number']
    global Chapter
    Chapter = str(Chapter_no) + "." + str(Chapter_name)

    l = os.listdir("dataset/quiz_data/" + Class + "/" + str(Subject))
    Chapter = str(Chapter_no) + "." + str(Chapter_name)
    if Chapter not in l:
        os.mkdir("dataset/quiz_data/" + Class + "/" + str(Subject) + "/" + str(Chapter))

    global Quiz_no
    l = os.listdir("dataset/quiz_data/" + Class + "/" + str(Subject) + "/" + str(Chapter))
    Quiz_no = len(l) + 1

    global No_of_questions
    No_of_questions = int(request.form['No_of_questions'])

    global i
    i += 1
    return render_template('create_quiz/index.html',No_of_questions = No_of_questions, Chapter_name = Chapter,i=i)

@app.route('/f2',methods = ['GET','POST'])
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
    return render_template('create_quiz/index.html',No_of_questions = No_of_questions , Chapter_name = Chapter, i=i)

@app.route('/result',methods = ['GET','POST'])
def result():

    que = request.form.get('question')
    options = request.form.get('options')
    answer = request.form.get('answer')
    explanation = request.form.get('explanation')

    preprocessing(que,options,answer,explanation)

    global dQ,dO

    df = pd.concat([d_Que,d_Opt,d_Ans,d_Exp],axis=1)
    df.columns = ['Question','Options','Answer','Explanation']

    global Class,subject,Chapter,Quiz_no
    df.to_csv("dataset/quiz_data/" + str(Class) + "/" + str(Subject) + "/" + str(Chapter) + "/" + str(Quiz_no) + ".csv",index=False)
    return 'Quiz created with name : {}'.format(Chapter[2:])

if __name__ == '__main__':
    app.run(debug=True)
