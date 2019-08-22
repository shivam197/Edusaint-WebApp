from flask import Flask,render_template,url_for,request,redirect
from flask_ckeditor import CKEditor

init_app = Flask(__name__)

ckeditor = CKEditor(init_app)
from App.Quiz.Create.create_quiz import cq_app
from App.Quiz.Play.play_quiz import quiz_app

from App.Qna.search.ocr import qna_search
from App.Qna.update.update_que import update_que

init_app.register_blueprint(Quiz.Create.create_quiz.cq_app)
init_app.register_blueprint(Quiz.Play.play_quiz.quiz_app)

init_app.register_blueprint(Qna.search.ocr.qna_search)
init_app.register_blueprint(Qna.update.update_que.update_que)

@init_app.route('/')
def f():
    return render_template('start.html')

@init_app.route('/q',methods=['GET','POST'])
def f1():
    req = request.form['option']

    if req == 'Play Quiz':
        return redirect('/choose_quiz')
    elif req == 'Search Question':
        return 'Broken right now !'

    if req == 'Admin':
        return render_template('start_admin.html')
    elif req == 'Create Question':
        return redirect('/admin/upload')
    elif req == 'Create Quiz':
        return redirect('/admin/create')
