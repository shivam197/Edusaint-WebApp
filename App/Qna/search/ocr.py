from flask import Flask,request,url_for,render_template,redirect,Blueprint,flash
import pytesseract
import numpy as np
from PIL import Image
from difflib import SequenceMatcher
import os
import cv2

dir = os.path.dirname(os.path.abspath(__name__)) + '/App/'

qna_search = Blueprint("qna_play", __name__)

ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']

#pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

@qna_search.route('/upload_question',methods =['GET','POST'])
def get():
    return render_template('ncert_solutions/search/index.html')

@qna_search.route('/answer',methods=['GET','POST'])
def result():
    file = request.files['Image']

    if file.filename.split('.')[1].lower() not in ALLOWED_EXTENSIONS:
        return redirect("/upload_question")

    img = Image.open(request.files['Image'])
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    text = ''
    i = 1
    while len(text) == 0 and i<14:
        img = cv2.medianBlur(img, ksize = i)
        text = pytesseract.image_to_string(img, lang='eng')
        text = text.replace('\n',' ')
        i+=2

    df = np.load('App/dataset/qna_data/Data.npz')
    if len(df['Question']) == 0:
        return 'Error! No questions found in database!'
    #match = []
    maximum = 0
    position = -1
    for i in range(len(df['Question'])):
        que = str(df['Question'][i])
        #match.append(SequenceMatcher(None,que,text).ratio())
        if maximum < (SequenceMatcher(None,que,text).ratio()):
            position = i
            maximum = (SequenceMatcher(None,que,text).ratio())

    if position == -1:
        return render_template('ncert_solutions/search/error.html')

    return render_template('ncert_solutions/search/result.html', Link = df['Link'][position] , text = text, i = position ) #, match = match)
