from ast import Bytes
from curses.ascii import alt
import re
from django.conf import settings
from django.shortcuts import render
from django.http import QueryDict
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import cv2 as cv
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from io import BytesIO
#./models/name_of_model
# Create your views here.
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
        for i in images:
            im = cv.imread(i)
            alteredIm = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            alteredImages.append(alteredIm)
            names.append(i.split('/')[-1])
        for count,img in enumerate(alteredImages):
            im = Image.fromarray(img)
            buffer = BytesIO()
            im.save(buffer, format='png')
            image_png = buffer.getvalue()
            tempim = default_storage.save('lap'+names[count], ContentFile(image_png))
            donePaths.append("./media/"+tempim)
            context = {'donePaths': donePaths}
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
    
    
    return render(request, 'composite_app/home.html', context)

def viewDB(request):
    listOfImages = os.listdir('./media/')
    listOfImagePaths = ['./media/'+i for i in listOfImages]
    