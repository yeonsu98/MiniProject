from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
from keras.models import load_model
from django.core.files.storage import FileSystemStorage
import joblib

# from pybo.model import Result
from .models import Result
from ml.models import *

# Create your views here.

logger = logging.getLogger('mylogger')

def index(request):
        ml_model = ML_Model.objects.get(is_selected=True)
        print('ml_model.title ',ml_model.title)
        if ml_model.title != '':
            context = {
                'selectedModel' : ml_model.title
            }
        else:
            context = {
                'selectedModel' : ''
            }
        return render(request, 'language/index.html',context)
        # return render(request, 'language/index.html')

def upload(request):
    if request.method == 'POST' and request.FILES:
        print('='*50)
        print('1')
        
        # form 에서 받은 값 : file list, answer[]
        file = request.FILES.getlist('files')
        print('files >> ',file)
        print('file length >> ',len(file))
        print('file[0] >> ',file[0])
       
        # class names 준비 & model 불러오기
        class_names = list(string.ascii_lowercase)
        class_names = np.array(class_names)
        
        # model_path = settings.MODEL_DIR +'/rf_pickle.pickle'
        ml_model = ML_Model.objects.get(is_selected=True)
        model_path = ml_model.model_file.path
        print("ml_model >> ",ml_model.title)
        print("ml_model.model_file >> ", model_path)
        if model_path.split('.')[1] == 'h5':
            print("aaaaa")
            model = load_model(model_path)     
        else:
            print("bbbbbb")
            model = joblib.load(model_path) 
        
        
        # 파일 저장
        pred2 = []
        resultList = []
        answers = request.POST.getlist('answer[]')
        
        for i,el in enumerate(file):
            fs = FileSystemStorage(location='media/tmp', base_url='media/tmp')
            filename = fs.save(file[i].name, file[i])
            print('el : ', el)
            print('filename : ',filename)
            
            img = cv2.imread(fs.url(filename), cv2.IMREAD_GRAYSCALE)
            print("111 >>> ", img)                 
            
            img = cv2.resize(img, (28,28))
            img = img/255.
            
            result = Result()
            result.answer = answers[i]
            result.image = file[i]
            result.pub_date = timezone.datetime.now()
                        
            if model_path.split('.')[1] == 'h5':            
                # Upload Image 전처리
                img = img.reshape(1,28,28,1)
                pred = model.predict(img) 
                pred2.append(pred.argmax(axis=1))
                
                if result.answer != class_names[pred2[i][0]][0]:
                    result.ret = '틀렸습니다!'
                else:  
                    result.ret = '맞았습니다!'
                result.result = class_names[pred2[i][0]][0]
                
                # Evaluation 갱신
                ml_model.evaluate(result.answer, class_names[pred2[i][0]][0])
            
            else:
                img = img.reshape(-1,784)
                pred = model.predict(img) 
                pred2.append(pred)
                if result.answer != class_names[int(pred2[i][0][0])][0]:
                    result.ret = '틀렸습니다!'
                else:  
                    result.ret = '맞았습니다!'
                result.result = class_names[int(pred2[i][0][0])][0]

                # Evaluation 갱신
                ml_model.evaluate(result.answer, class_names[int(pred2[i][0][0])][0])
            
    
            print("result.answer : ",result.answer)
    
            result.save()
            resultList.append(result)
            
        print("*"*50)
        
    
        context = {
            'resultList': resultList,
            'selectedModel' : ml_model.title
        }

    

    # http method의 GET은 처리하지 않는다. 사이트 테스트용으로 남겨둠.
    else:
        test = request.GET['test']
        logger.error(('Something went wrong!!',test))

    return render(request, 'language/result.html', context)