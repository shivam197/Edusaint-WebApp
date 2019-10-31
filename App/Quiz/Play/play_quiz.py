from flask import Blueprint, render_template, request, Flask, flash,redirect
import random, copy
import pandas as pd
import os
import numpy as np

quiz_app = Blueprint('quiz',__name__)
#quiz_app = Flask(__name__)

play_df = pd.DataFrame()
play_questions = {}
play_correct_answer = {}
play_explanation = {}

play_Class = ""
play_Subject = ""
play_Chapter = ""
play_dir = ""
play_complete_dir = ""

def init():
    global play_df,play_questions,play_correct_answer,play_explanation,play_Class,play_Subject,play_Chapter,play_dir
    play_df = pd.DataFrame()
    play_questions = {}
    play_correct_answer = {}
    play_explanation = {}
    play_Class = ""
    play_Subject = ""
    play_Chapter = ""
    play_dir = os.path.join(str(os.path.dirname(os.path.abspath(__name__))),"App")

def clear():
    global play_df,play_questions,play_correct_answer,play_explanation,play_Class,play_Subject,play_Chapter,play_dir
    del play_df
    del play_questions
    del play_correct_answer
    del play_explanation
    del play_Class
    del play_Subject
    del play_Chapter
    del play_dir


def open_quiz(directory):
    global play_df
    global play_questions
    global play_correct_answer
    global play_explanation

    play_df = pd.read_csv(directory)

    for i in range(play_df.shape[0]):
        play_questions[play_df.iloc[i,0]] = play_df.iloc[i,1].split('#')[:-1]
        play_correct_answer[play_df.iloc[i,0]] = play_df.iloc[i,2]
        play_explanation[play_df.iloc[i,0]] = play_df.iloc[i,3]



@quiz_app.route('/choose_quiz')
def play_quiz_init():
    global play_dir
    init()
    if "quiz_data" not in os.listdir(os.path.join(play_dir,"dataset")):
        os.mkdir(os.path.join(play_dir,"dataset","quiz_data"))
        
    play_dir = os.path.join(play_dir,"dataset","quiz_data")
    Classes = os.listdir(play_dir)

    if len(Classes) == 0:
        return render_template('Quiz/play/error.html')
    return render_template('Quiz/play/intro.html', Classes = Classes, i=1)

@quiz_app.route('/choose_quiz/subject', methods = ['GET','POST'])
def play_quiz_choose_sub():
    global play_Class,play_dir
    if request.method == "POST" or request.method == "post":
        play_Class = str(request.form['Class'])
    play_dir = os.path.join(play_dir,play_Class)
    Subjects = os.listdir(play_dir)
    if len(Subjects) == 0:
        return render_template('Quiz/play/error.html')
    return render_template('Quiz/play/intro.html', Subjects = Subjects, i=2)

@quiz_app.route('/choose_quiz/chapter', methods = ['GET','POST'])
def play_quiz_choose_ch():
    global play_Subject,play_Class,play_dir
    if request.method == "POST" or request.method == "post":
        play_Subject = str(request.form['Subject'])
    play_dir = os.path.join(play_dir,play_Subject)
    Chapters = os.listdir(play_dir)
    if len(Chapters) == 0:
        return render_template('Quiz/play/error.html')
    return render_template('Quiz/play/intro.html', Chapters = Chapters, i=3)

@quiz_app.route('/quiz',methods=['GET','POST'])
def play_quiz():
    global play_Class,play_Subject,play_Chapter,play_dir

    play_Chapter = str(request.form['Chapter'])
    play_dir = os.path.join(play_dir,play_Chapter)
    l = os.listdir(play_dir)

    if len(l)>0:
        n = np.random.randint(1,len(l)+1)

        play_dir = os.path.join(play_dir,(str(n) + '.csv'))
        open_quiz(play_dir)

    if len(play_questions) == 0:
        return render_template('Quiz/play/error.html')
    return render_template('Quiz/play/index.html', questions = play_questions, topic=play_Chapter[2:])


@quiz_app.route('/quiz_result', methods=['POST'])
def play_quiz_answers():
    global play_questions,correct_answer,play_explanation
    correct = 0
    answered = {}
    for i in play_questions:
        try:
            ans =  request.form[i]
        except:
            ans = ""

        answered[i] = [0,ans]
        if ans == play_correct_answer[i].lower():
            correct += 1
            answered[i] = [1,ans]

    explanation_temp = play_explanation

    questions_temp = play_questions

    correct_answer_temp = play_correct_answer

    clear()
    return render_template('Quiz/play/result.html',explanation = explanation_temp, answered = answered, questions = questions_temp, correct = correct, correct_answer = correct_answer_temp)
