from ast import Bytes
from curses.ascii import alt
import re
import numpy as np
from django.conf import settings
from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import dlib
import random
import datetime
import cv2 as cv
from PIL import Image
from django.conf import settings
import imutils
from helpers.face_utils import FaceAlignerNoCrop
from helpers.face_utils import rect_to_bb
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from io import BytesIO
#./models/name_of_model
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./models/shape_predictor_68_face_landmarks.dat")
fa = FaceAlignerNoCrop(predictor, desiredFaceWidth=2048)
# Create your views here.
def average(arr):
    covers = []
    for j in arr:
        cover = None
        cover = cv.imread(j)
        if cover is not None:
            cover = cv.resize(cover, (1200, 1200)).flatten()
            covers.append(cover)
    avg = np.average(covers, axis=0).reshape((1200, 1200, 3)).astype("uint8")
    im = Image.fromarray(avg)
    buffer = BytesIO()
    im.save(buffer, format='png')
    image_png = buffer.getvalue()
    tempim = default_storage.save('average_'+datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '.png', ContentFile(image_png))
    return tempim        

def center_face (filename):
    faces = []
    if ".jpg" in filename or ".png" in filename or ".jpeg" in filename or ".JPG" in filename:
        image = cv.imread(filename)
        image = imutils.resize(image, width=940)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        rects = detector(gray, 2)
        for rect in rects:
            faceAligned = fa.align(image, gray, rect)
            faces.append(faceAligned)
    return faces
	
def home(request):
    listOfImages = os.listdir('./media/stars/')
    listOfImagePaths = ['./media/stars/'+i for i in listOfImages]
    context={'listOfImagePaths':listOfImagePaths}
    return render(request, 'composite_app/home.html', context)

@csrf_exempt
def predictImage(request):
    context = {}
    tmp_file = ''
    if request.POST:
        images = request.POST
        images = json.loads(json.dumps(dict(images)))["images[]"] 
        donePaths = []
        alteredImages = []
        names = []      
        for count,i in enumerate(images):
            faces = center_face(i)
            facesToAppend = []
            for facenum,face in enumerate(faces):
                im = Image.fromarray(face)
                buffer = BytesIO()
                im.save(buffer, format='png')
                image_png = buffer.getvalue()
                tempim = default_storage.save('lap'+ str(facenum) + i.split('/')[-1], ContentFile(image_png))
                alteredImages.append("./media/"+tempim)
        tmp = average(alteredImages)
        context = {'tmp': "./media/"+tmp}
    if request.FILES:
        fileObj = request.FILES['filePath']
        path = default_storage.save(fileObj.name, ContentFile(fileObj.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)
        fs = FileSystemStorage()
        tmp_file = fs.url(path)
        test_image = '.'+tmp_file
        img = cv.imread(test_image)
        laplacian = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        im = Image.fromarray(laplacian)
        buffer = BytesIO()
        im.save(buffer, format='png')
        image_png = buffer.getvalue()
        path2 = default_storage.save('lap'+path, ContentFile(image_png))
        tmp_file = fs.url(path2)
        context={'filePathName': tmp_file}
    
    
    return render(request, 'composite_app/done.html', context)

def viewDB(request):
    listOfImages = os.listdir('./media/')
    listOfImagePaths = ['./media/'+i for i in listOfImages]
    