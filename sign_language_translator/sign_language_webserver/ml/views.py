from django.shortcuts import render, redirect
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from .models import *
from .forms import *

logger = logging.getLogger('mylogger')


def list(request):
    model_list = ML_Model.objects.all()
    return render(request, 'ml/list.html', {'model_all': model_list})


def ml_model_create(request):
    if request.method == 'POST' and request.FILES:
        # form = MakeMLModelForm(request.POST)
        # title', 'version', 'is_selected', 'model_file'
        ml_model = ML_Model()        
        file = request.FILES.getlist('files')
        ml_model.title = request.POST.get('title')
        ml_model.version = request.POST.get('version')
        
        print("form >>>> ", request.POST.get('title'))
        print("form >>>> ", request.POST.get('version'))
        print("form >>>> ", request.POST.get('is_selected'))
        # print('files >> ',file)
        print('file length >> ',len(file))
        print('file[0] >> ',file[0])
       
        fs = FileSystemStorage(location='media/models', base_url='media/models')
        fs.save(file[0].name, file[0])
            
        
        if request.POST.get('is_selected') =='on':
            ml_model.is_selected = 1
        else:
            ml_model.is_selected = 0
        
        ml_model.model_file = file[0]
        
        ml_model.save()
        # if form.is_valid():
        #     print('aaaa')
        #     # ml_model = form.save()
        # else:
        #     print(">> Error")
        #     print(form.errors)

        return redirect ('ml:list')
    else:
        print('bbbb')
        form = MakeMLModelForm()
        return render(request, 'ml/ml_model_form.html', {'form': form})
