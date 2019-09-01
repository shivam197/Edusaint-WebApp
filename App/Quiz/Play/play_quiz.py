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
    global df,questions,correct_answer,explanation,Class,Subject,Chapter
    df = pd.DataFrame()
    questions = {}
    correct_answer = {}
    explanation = {}
    Class = ""
    Subject = ""
    Chapter = ""

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


dir = str(os.path.dirname(os.path.abspath(__name__))) + "/App/"
@quiz_app.route('/choose_quiz')
def choose():
    global dir
    init()
    Classes = os.listdir(dir + 'dataset/quiz_data/')
    return render_template('Quiz/play/intro.html', Classes = Classes, i=1) #, dir = (dir + 'dataset/quiz_data/'))

@quiz_app.route('/choose_quiz/subject', methods = ['GET','POST'])
def choose_sub():
    global Class,dir
    if request.method == 'POST':
        Class = request.form['Class']
    Subjects = os.listdir(dir + 'dataset/quiz_data/' + str(Class))
    return render_template('Quiz/play/intro.html', Subjects = Subjects,i =2) #, dir = (dir + 'dataset/quiz_data/' + str(Class)))

@quiz_app.route('/choose_quiz/chapter', methods = ['GET','POST'])
def choose_ch():
    global Subject,Class,dir
    if request.method == 'POST':
        Subject = request.form['Subject']
    Chapters = os.listdir(dir + 'dataset/quiz_data/' + str(Class) + "/" + str(Subject))
    return render_template('Quiz/play/intro.html', Chapters = Chapters, i=3) #, dir = (dir + 'dataset/quiz_data/' + str(Class) + "/" + str(Subject)))

@quiz_app.route('/quiz',methods=['GET','POST'])
def quiz():
    global Class,Subject,Chapter,dir

    Chapter = request.form['Chapter']
    l = os.listdir(dir + "dataset/quiz_data/" + str(Class) + "/" + str(Subject) + "/" + str(Chapter))
    if len(l)>0:
        n = np.random.randint(1,len(l)+1)
    directory = dir + "dataset/quiz_data/" + str(Class) + "/" + str(Subject) + "/" + str(Chapter) + "/" + str(n) + ".csv"
    open_quiz(directory)
    global df
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
