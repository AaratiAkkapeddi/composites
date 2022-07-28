import re
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
#./models/name_of_model
# Create your views here.
def home(request):
    context={'filePathName':0}
    return render(request, 'composite_app/home.html', context)

@csrf_exempt
def predictImage(request):
    
    fileObj = request.FILES['filePath']
    path = default_storage.save(fileObj.name, ContentFile(fileObj.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    fs = FileSystemStorage()
    tmp_file = fs.url(path)
    test_image = '.'+tmp_file
    context={'filePathName':tmp_file}
    return render(request, 'composite_app/home.html', context)

def viewDB(request):
    listOfImages = os.listdir('./media/')
    listOfImagePaths = ['./media/'+i for i in listOfImages]
    