from flask import Blueprint, render_template, request, Flask
import random, copy
import pandas as pd
import os
import numpy as np

quiz_app = Blueprint('quiz',__name__)
#quiz_app = Flask(__name__)

df = pd.DataFrame()
questions = {}
correct_answer = {}
explanation = {}

Class = ""
Subject = ""
Chapter = ""

def init():
    global df,questions,correct_answer,explanation,Class,Subject,Chapter,dir
    df = pd.DataFrame()
    questions = {}
    correct_answer = {}
    explanation = {}
    Class = ""
    Subject = ""
    Chapter = ""
    dir = os.path.join(str(os.path.dirname(os.path.abspath(__name__))),"App")

def open_quiz(directory):
    global df
    global questions
    global correct_answer
    global explanation

    df = pd.read_csv(directory)

    for i in range(df.shape[0]):
        questions[df.iloc[i,0]] = df.iloc[i,1].split('#')[:-1]
        correct_answer[df.iloc[i,0]] = df.iloc[i,2]
        explanation[df.iloc[i,0]] = df.iloc[i,3]


dir = os.path.join(str(os.path.dirname(os.path.abspath(__name__))),"App")
complete_dir = dir
@quiz_app.route('/choose_quiz')
def choose():
    global dir,complete_dir
    init()
    complete_dir = os.path.join(dir,"dataset","quiz_data")
    Classes = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Classes = Classes, i=1) #, dir = complete_dir)

@quiz_app.route('/choose_quiz/subject', methods = ['GET','POST'])
def choose_sub():
    global Class,dir,complete_dir
    if request.method == 'POST':
        Class = str(request.form['Class'])
    complete_dir = os.path.join(dir,"dataset","quiz_data",Class)
    Subjects = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Subjects = Subjects,i =2) #, dir = complete_dir)

@quiz_app.route('/choose_quiz/chapter', methods = ['GET','POST'])
def choose_ch():
    global Subject,Class,dir,complete_dir
    if request.method == 'POST':
        Subject = str(request.form['Subject'])
    complete_dir = os.path.join(dir,"dataset","quiz_data",Class,Subject)
    Chapters = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Chapters = Chapters, i=3) #, dir =complete_dir)

@quiz_app.route('/quiz',methods=['GET','POST'])
def quiz():
    global Class,Subject,Chapter,dir,complete_dir

    Chapter = str(request.form['Chapter'])
    complete_dir = os.path.join(complete_dir,Chapter)
    l = os.listdir(complete_dir)
    if len(l)>0:
        n = np.random.randint(1,len(l)+1)

    complete_dir = os.path.join(complete_dir,(str(n) + '.csv'))
    open_quiz(complete_dir)

    return render_template('Quiz/play/index.html', questions = questions, topic= Chapter[2:])


@quiz_app.route('/quiz_result', methods=['POST'])
def quiz_answers():
    correct = 0
    answered = {}
    for i in questions:
        try:
            ans =  request.form[i]
        except:
            ans = ""

        answered[i] = [0,ans]
        if ans == correct_answer[i].lower():
            correct += 1
            answered[i] = [1,ans]


    return render_template('Quiz/play/result.html',explanation = explanation, answered = answered, questions = questions, correct = correct, correct_answer = correct_answer)
