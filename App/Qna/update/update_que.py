from flask import Flask,render_template,request,Blueprint
from flask_ckeditor import CKEditor
import os
import pandas as pd
from PIL import Image


update_que = Blueprint('update_que',__name__)
#update_que = Flask(__name__)
dir = os.path.dirname(os.path.abspath(__name__))+'/App/'
link = ""
df  = pd.read_csv(dir+'dataset/qna_data/Data.csv')

@update_que.route('/admin/upload')
def f():

    return render_template('/ncert_solutions/update/intro.html')

@update_que.route('/admin/upload_que', methods = ['GET','POST'])
def f1():
    global dir,link

    l = os.listdir(dir + 'dataset/qna_data')

    Class = "Class " + str(request.form['class'])
    if Class not in l:
        os.mkdir(dir + "dataset/qna_data/" + str(Class))

    Subject = request.form['subject'].lower()
    l = os.listdir(dir + 'dataset/qna_data/'+ Class)
    if Subject not in l:
        os.mkdir(dir + "dataset/qna_data/" + Class + "/" + str(Subject))

    Chapter_name = request.form['Chapter_name'].lower()
    Chapter_no = request.form['chapter_number']

    Chapter = str(Chapter_no) + ". " + str(Chapter_name[0].upper()) + str(Chapter_name[1:])

    l = os.listdir(dir + "dataset/qna_data/" + Class + "/" + str(Subject))

    if Chapter not in l:
        os.mkdir(dir + "dataset/qna_data/" + Class + "/" + str(Subject) + "/" + str(Chapter))

    link = "/App/dataset/qna_data/" + Class + "/" + str(Subject) + "/" + str(Chapter) + "/"
    return render_template('ncert_solutions/update/index.html', Chapter_name = Chapter)

@update_que.route('/admin/upload_que_',methods = ['GET','POST'])
def f2():
    global df,dir,link
    question = request.form.get('question')
    question = question.replace('<p>','')
    question = question.replace('</p>','')
    question = question.replace('&nbsp;',' ')
    question = question.replace('\r\n',' ')
    question = question.replace('<br>',' ')

    img = Image.open(request.files['Image'])
    complete_dir = os.path.dirname(os.path.abspath(__name__)) + link
    name = len(os.listdir(complete_dir)) + 1
    img.save(complete_dir +  str(name) + '.png')
    link = link + str(name) + '.png'

    d = pd.DataFrame([[str(question),str(link)]])
    d.columns = ['Questions','Link']
    df = df.append(d,ignore_index= True)
    df.to_csv(dir + '/Dataset/qna_data/Data.csv',index=False)
    return render_template('ncert_solutions/update/result.html')
