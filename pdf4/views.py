from django.shortcuts import render, redirect
from .forms import MergeForm
from .pdf4 import mergefunction
from django.core.files.storage import FileSystemStorage

def home_view(request):
		return render(request, 'index.html')


def merge_view(request):
    if request.method == 'POST' and request.FILES['file1'] and request.FILES['file2']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        file1name = fs.save(file1.name, file1)  #сохраняем файлы из формы
        file2name = fs.save(file2.name, file2)
        resulturl = mergefunction('./pdf4/media/'+ file1name, './pdf4/media/'+ file2name)   #вызываем функцию для объединения файлов из pdf4.py, на выходе из которой получаем url результата
        fs.delete(file1name)    #удаляем исходные файлы
        fs.delete(file2name)
        return render(request, 'merge.html', {
            'resulturl': resulturl
        })
    return render(request, 'merge.html')





