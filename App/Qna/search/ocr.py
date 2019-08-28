from flask import Flask,request,url_for,render_template,redirect,Blueprint
import pytesseract
import pandas as pd
from PIL import Image
from difflib import SequenceMatcher
import os

dir = os.path.dirname(os.path.abspath(__name__)) + '/App/'

df = pd.read_csv('App/dataset/qna_data/Data.csv')
qna_search = Blueprint("qna_play", __name__)

pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

@qna_search.route('/upload_question',methods =['GET','POST'])
def get():
    return "Inside ocr.py"
    return render_template('ncert_solutions/search/index.html')

@qna_search.route('/answer',methods=['GET','POST'])
def result():
    img = Image.open(request.files['Image'])
    text = pytesseract.image_to_string(img, lang='eng')
    match = []
    for i in range(df.shape[0]):
        que = df['Questions'][i]
        match.append(SequenceMatcher(None,que,text).ratio())

    i = match.index(max(match))
    return render_template('ncert_solutions/search/result.html', Link = df['Link'][i])
