from django.shortcuts import render, redirect
from .forms import MergeForm
from .pdf4 import mergefunction, insertfunction, getnumpagesfunction, split1function
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





def insert_view(request):
    if 'file1_cookie' not in request.session:
        request.session['file1_cookie'] = []   #имя первого файла
    if 'file2_cookie' not in request.session:
        request.session['file2_cookie'] = []   #имя второго файла
    if request.method == 'POST':
        if 'button_111' in request.POST:
            fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
            file1 = request.FILES['file1']
            file2 = request.FILES['file2']
            file1name = fs.save(file1.name, file1)  #сохраняем файлы из формы
            file2name = fs.save(file2.name, file2)
            request.session['file1_cookie'] = file1name
            request.session['file2_cookie'] = file2name
            insert_position = 9999
            return render(request, 'insert.html', {
                'insert_position': insert_position
                })
        else:
            file1name = ''.join(request.session['file1_cookie'])
            file2name = ''.join(request.session['file2_cookie'])
            resulturl = ''
            insert_position = request.POST['select_position']
    # если в строчке ниже убрать явное приведение к типу int то появится ошибка django slice indices must be integers or None or have an __index__ method
            resulturl = insertfunction('./pdf4/media/'+ file1name, './pdf4/media/'+ file2name, int(insert_position))   #вызываем функцию для объединения файлов из pdf4.py, на выходе из которой получаем url результата
            fs = FileSystemStorage()
            fs.delete(file1name)    #удаляем исходные файлы
            fs.delete(file2name)
            del request.session['file1_cookie']
            del request.session['file2_cookie']
            return render(request, 'insert.html', {
                'resulturl': resulturl,
                'insert_position': insert_position
                })
    else:
        return render(request, 'insert.html')


def split_1_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']
        file1name = fs.save(file1.name, file1)  #сохраняем файл из формы
        resulturl = split1function('./pdf4/media/'+ file1name)   #вызываем функцию для разделения файла на отдельные страницы из pdf4.py, на выходе из которой получаем url для скачивания архива со страницами
        fs.delete(file1name)    #удаляем исходный файлы
        return render(request, 'split-1.html', {
            'resulturl': resulturl
        })
    return render(request, 'split-1.html')



