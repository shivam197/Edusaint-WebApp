from flask import Blueprint, render_template, request, Flask,redirect
import random, copy
import pandas as pd
import os
import numpy as np
import shutil

del_app = Blueprint('Delete_quiz',__name__)
#quiz_app = Flask(__name__)

Class = ""
Subject = ""
Chapter = ""
dir = os.path.join(str(os.path.dirname(os.path.abspath(__name__))),"App")
Num = 0

def init():
    global Class,Subject,Chapter,dir
    Class = ""
    Subject = ""
    Chapter = ""
    Num = 0
    dir = os.path.join(str(os.path.dirname(os.path.abspath(__name__))),"App")

@del_app.route('/admin/delete', methods = ['GET','POST'])
def choice():
    init()
    return render_template('Delete/intro.html', op = 1)

@del_app.route('/admin/choice',methods = ['GET','POST'])
def choose():
    choice = request.form['option']
    global Class,Subject,Chapter,Num,dir

    if choice == 'Delete Quiz':
        dir = os.path.join(dir,'dataset','quiz_data')
        return render_template('Delete/intro.html', op = 2)

    elif choice == 'Delete Question Database':
        np.savez(os.path.join(dir,'dataset','qna_data',"Data.npz"),Question = [], Link = [])
        try:
            shutil.rmtree(os.path.join(dir,'static'))
        except:
            pass
        #os.mkdir(os.path.join(dir,'static'))
        return render_template('Delete/result.html', msg = 'Question database cleared')

    elif choice == 'Delete by class':
        Class = 1
        Subject = 0
        Chapter = 0
        Num = 0
        return redirect('/admin/choose_quiz')
    elif choice == 'Delete by subject':
        Class = 1
        Subject = 1
        Chapter = 0
        Num = 0
        return redirect('/admin/choose_quiz')
    elif choice == 'Delete by chapter':
        Class = 1
        Subject = 1
        Chapter = 1
        Num = 0
        return redirect('/admin/choose_quiz')
    elif choice == 'Delete individually':
        Class = 1
        Subject = 1
        Chapter = 1
        Num = 1
        return redirect('/admin/choose_quiz')


@del_app.route('/admin/choose_quiz', methods = ['GET','POST'])
def choose1():
    global dir
    if len(os.listdir(dir)) == 0:
        return render_template('Delete/result.html',msg = "no_class")
    Classes = os.listdir(dir)
    return render_template('Delete/index.html', Classes = Classes, i=1)

@del_app.route('/admin/choose_quiz/subject', methods = ['GET','POST'])
def choose_sub():
    global Class,Subject,Chapter,Num,dir
    if request.method == "POST" or request.method == "post":
        Class = str(request.form['Class'])
    dir = os.path.join(dir,Class)
    if len(os.listdir(dir)) == 0:
        os.rmdir(dir)
        return render_template('Delete/result.html',msg = "no_subject",Class = Class)
    elif Subject == 0:

        return render_template('Delete/index.html', Class = Class,Subject = 0, i=5)

    Subjects = os.listdir(dir)
    return render_template('Delete/index.html', Subjects = Subjects, i=2)

@del_app.route('/admin/choose_quiz/chapter', methods = ['GET','POST'])
def choose_ch():
    global Class,Subject,Chapter,Num,dir
    if request.method == "POST" or request.method == "post":
        Subject = str(request.form['Subject'])
    dir = os.path.join(dir,Subject)
    if len(os.listdir(dir)) == 0:
        os.rmdir(dir)
        return render_template('Delete/result.html',msg = "no_chapter",Class = Class,Subject=Subject)
    elif Chapter == 0:

        return render_template('Delete/index.html',Class = Class,Subject=Subject,Chapter = 0,i=5)
    Chapters = os.listdir(dir)
    return render_template('Delete/index.html', Chapters = Chapters, i=3)

@del_app.route('/admin/choose_quiz/quiz_number',methods = ['GET','POST'])
def choose_num():
    global Class,Subject,Chapter,Num,dir
    if request.method == "POST" or request.method == "post":
        Chapter = str(request.form['Chapter'])
    dir = os.path.join(dir,Chapter)
    if len(os.listdir(dir)) == 0:
        os.rmdir(dir)
        return render_template('Delete/result.html',msg = "no_quiz", Subject=Subject,Chapter=Chapter,Class=Class)

    elif Num == 0:

        return render_template('Delete/index.html', Subject=Subject,Chapter=Chapter,Class=Class, Num = 0,i=5)
    Num = []
    for i in os.listdir(dir):
        Num.append(i.split('.')[0])
    return render_template('Delete/index.html', Num = Num, i=4)

@del_app.route('/admin/delete/prompt',methods=['GET','POST'])
def prompt():
    global Subject,Class,dir,Chapter,Num
    if request.method == 'POST' or request.method == 'post':
        Num = str(request.form['Quiz_Number'])
        dir = os.path.join(dir,(Num + ".csv"))
    return render_template('Delete/index.html',Subject=Subject,Chapter=Chapter,Class=Class,Num = Num, i=5)

@del_app.route('/admin/delete/result', methods = ['GET','POST'])
def result():
    global Subject,Class,dir,Chapter,Num
    if request.method == 'POST' or request.method == 'post':
        choice = request.form['confirmation']
    if choice == 'Yes':
        if Num!=0:
            os.remove(dir)
        else:
            shutil.rmtree(dir)
        return render_template('Delete/result.html',Subject=Subject,Chapter=Chapter,Class=Class, Num = Num)
    else:
        redirect('/admin/delete')
