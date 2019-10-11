from flask import Flask,render_template,request,Blueprint
from flask_ckeditor import CKEditor
import os
import numpy as np
from PIL import Image


update_que = Blueprint('update_que',__name__)
#update_que = Flask(__name__)

ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']
dir = os.path.join(os.path.dirname(os.path.abspath(__name__)),'App')
link = ""

Class = ''
Subject = ''
Chapter_no = ''
Chapter_name = ''
'''
@update_que.route('/admin/update_que')
def function():
    return render_template('/ncert_solutions/update/intro.html')
'''
@update_que.route('/admin/upload')
def f():
    l = os.listdir(dir)
    if 'static' not in l:
        os.mkdir(os.path.join(dir,'static'))
    return render_template('/ncert_solutions/update/upload.html')

@update_que.route('/admin/upload_que', methods = ['GET','POST'])
def f1():
    global dir,link,Class,Subject,Chapter_no,Chapter_name

    l = os.listdir(os.path.join(dir,'static'))
    if request.method == 'POST':
        Class = "Class " + str(request.form['class'])

    if Class not in l:
        os.mkdir(os.path.join(dir ,"static" ,str(Class)))

    if request.method == 'POST':
        Subject = request.form['subject'].lower()

    l = os.listdir(os.path.join(dir,'static',Class))
    if Subject not in l:
        os.mkdir(os.path.join(dir,"static",Class,str(Subject)))

    if request.method == 'POST':
        Chapter_name = request.form['Chapter_name'].lower()
        Chapter_no = request.form['chapter_number']

    Chapter = str(Chapter_no) + ". " + str(Chapter_name[0].upper()) + str(Chapter_name[1:])

    l = os.listdir(os.path.join(dir,"static",Class,str(Subject)))

    if Chapter not in l:
        os.mkdir(os.path.join(dir,"static",Class,str(Subject),str(Chapter)))

    link = os.path.join("static",Class,str(Subject),str(Chapter))
    return render_template('ncert_solutions/update/index.html', Chapter_name = Chapter)

@update_que.route('/admin/upload_que_',methods = ['GET','POST'])
def f2():
    global dir,link
    question = request.form.get('question')
    question = question.replace('<p>','')
    question = question.replace('</p>','')
    question = question.replace('&nbsp;',' ')
    question = question.replace('\r\n',' ')
    question = question.replace('<br>',' ')
    question = question.replace('<h3>','')
    question = question.replace('</h3>','')

    df  = np.load(os.path.join(dir,'dataset','qna_data','Data.npz'))

    file = request.files['Image']

    if file.filename.split('.')[1].lower() not in ALLOWED_EXTENSIONS:
        return redirect("/admin/upload_que")

    img = Image.open(request.files['Image'])

    name = len(os.listdir(os.path.join(dir,link))) + 1
    link = os.path.join(link,(str(name) + '.png'))
    img.save(os.path.join(dir,link))
    question = np.append(df['Question'],question)
    link = np.append(df['Link'],link)
    #d = pd.DataFrame([[str(question),str('/' + link)]])
    #d.columns = ['Questions','Link']
    np.savez(os.path.join(dir,'dataset','qna_data','Data.npz'),Question = question, Link = link)
    #df = df.append(d,ignore_index= True)
    #df.to_csv(dir + '/dataset/qna_data/data.csv',index=False)
    return render_template('ncert_solutions/update/result.html')
'''
@update_que.route('/admin/delete')
def delete_function():
    pass
@quiz_app.route('/choose_quiz')
def choose():
    global dir,complete_dir
    init()
    complete_dir = os.path.join(dir,"dataset","quiz_data")
    Classes = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Classes = Classes, i=1)

@quiz_app.route('/choose_quiz/subject', methods = ['GET','POST'])
def choose_sub():
    global Class,dir,complete_dir
    if request.method == "POST" or request.method == "post":
        Class = str(request.form['Class'])
    complete_dir = os.path.join(dir,"dataset","quiz_data",Class)
    Subjects = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Subjects = Subjects, i=2)

@quiz_app.route('/choose_quiz/chapter', methods = ['GET','POST'])
def choose_ch():
    global Subject,Class,dir,complete_dir
    if request.method == "POST" or request.method == "post":
        Subject = str(request.form['Subject'])
    complete_dir = os.path.join(dir,"dataset","quiz_data",Class,Subject)
    Chapters = os.listdir(complete_dir)
    return render_template('Quiz/play/intro.html', Chapters = Chapters, i=3)

'''
