from flask import Flask,request,url_for,render_template,redirect,Blueprint,flash
import pytesseract
import numpy as np
from PIL import Image
from difflib import SequenceMatcher
import os
import cv2
import math
dir = os.path.join(os.path.dirname(os.path.abspath(__name__)),"App")
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
qna_search = Blueprint("qna_play", __name__)

ALLOWED_EXTENSIONS = ['png','jpg','jpeg','gif']

def kmeans(input_img, k, i_val):
    hist = cv2.calcHist([input_img],[0],None,[256],[0,256])
    img = input_img.ravel()
    img = np.reshape(img, (-1, 1))
    img = img.astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness,labels,centers = cv2.kmeans(img,k,None,criteria,10,flags)
    centers = np.sort(centers, axis=0)

    return centers[i_val].astype(int), centers, hist


@qna_search.route('/upload_question',methods =['GET','POST'])
def get():
    return render_template('ncert_solutions/search/index.html')

@qna_search.route('/answer',methods=['GET','POST'])
def result():
    file = request.files['Image']

    if file.filename.split('.')[1].lower() not in ALLOWED_EXTENSIONS:
        return redirect("/upload_question")

    img = Image.open(request.files['Image'])
    min_size = min(img.size[0],img.size[1])
    ratio = 1
    if min_size > 1000:
        ratio = math.ceil(min_size/1000)

    img = img.resize((int(img.size[0]/ratio),int(img.size[1]/ratio)))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    _, thresh = cv2.threshold(img, kmeans(input_img=img, k=8, i_val=2)[0], 255, cv2.THRESH_BINARY)
    text = pytesseract.image_to_string(thresh, lang='eng',config = tessdata_dir_config)

    if "qna_data" not in os.listdir(os.path.join(dir,"dataset")):
        os.mkdir(os.path.join(dir,"dataset","qna_data"))
        os.mkdir(os.path.join(dir,"static"))
        np.savez(os.path.join(dir,'dataset','qna_data',"Data.npz"),Question = [], Link = [])
        return 'Error! No questions found in database!'

    df = np.load('App/dataset/qna_data/Data.npz')
    if len(df['Question']) == 0:
        return 'Error! No questions found in database!'
    #match = []
    maximum = -1
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
