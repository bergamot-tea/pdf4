from django.shortcuts import render, redirect
from .forms import MergeForm
from .pdf4 import mergefunction, insertfunction, getnumpagesfunction, split1function, inimagesfunction, outimagesfunction, compressfunction, rotatefunction, inpdffunction, intextfunction
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


def in_images_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']  #передаем данные из формы в переменные
        format = request.POST['format1']
        file1name = fs.save(file1.name, file1)  #сохраняем файл из переменной
        resulturl = inimagesfunction('./pdf4/media/'+ file1name, format)   #вызываем функцию для преобразования файла в картинки из pdf4.py, на выходе из которой получаем url для скачивания архива со страницами
        fs.delete(file1name)    #удаляем исходный файлы
        return render(request, 'in-images.html', {
            'resulturl': resulturl
        })
    return render(request, 'in-images.html')

def out_images_view(request):
    if request.method == 'POST':
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        filename = dict.fromkeys([1,2,3,4,5]) #создем словарь для имен файлов, ключи словаря 1,2,3,4,5 а значения у ключей None
        if 'file1' in request.FILES:    #если вместо этого написать if request.FILES['file1']: то будет появляться ошибка в случае если поле пустое (если пользователь не выбрал файл)
            file1 = request.FILES['file1']
            filename[1] = fs.save(file1.name, file1)  #сохраняем файлы из формы, имена файлов записываем в словарь
        if 'file2' in request.FILES:
            file2 = request.FILES['file2']
            filename[2] = fs.save(file2.name, file2)  #сохраняем файлы из формы, имена файлов записываем в словарь
        if 'file3' in request.FILES:
            file3 = request.FILES['file3']
            filename[3] = fs.save(file3.name, file3)  #сохраняем файлы из формы, имена файлов записываем в словарь
        if 'file4' in request.FILES:
            file4 = request.FILES['file4']
            filename[4] = fs.save(file4.name, file4)  #сохраняем файлы из формы, имена файлов записываем в словарь
        if 'file5' in request.FILES:
            file5 = request.FILES['file5']
            filename[5] = fs.save(file5.name, file5)  #сохраняем файлы из формы, имена файлов записываем в словарь

        resulturl = outimagesfunction(filename[1], filename[2], filename[3], filename[4], filename[5])   #вызываем функцию для сбора PDF-файла из картинок, на выходе из которой получаем url результата
                                                           #В отличии от предыдущих функций, тут мы передаем значения словаря без добавления './pdf4/media/'
        if filename[1] != None:
            fs.delete(filename[1])    #удаляем исходный файлы
        if filename[2] != None:
            fs.delete(filename[2])
        if filename[3] != None:
            fs.delete(filename[3])
        if filename[4] != None:
            fs.delete(filename[4])
        if filename[5] != None:
            fs.delete(filename[5])

        return render(request, 'out-images.html', {
            'resulturl': resulturl
        })
    return render(request, 'out-images.html')



def compress_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']  #передаем данные из формы в переменные
        level = request.POST['level1']
        file1name = fs.save(file1.name, file1)  #сохраняем файл из переменной
        resulturl = compressfunction('./pdf4/media/'+ file1name, level)   #вызываем функцию для сжатия файла из pdf4.py, на выходе из которой получаем url для скачивания результата
        fs.delete(file1name)    #удаляем исходный файлы
        return render(request, 'compress.html', {
            'resulturl': resulturl
        })
    return render(request, 'compress.html')



def rotate_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']  #передаем данные из формы в переменные
        grad1 = request.POST['grad1']
        pages1 = request.POST['pages1']
        file1name = fs.save(file1.name, file1)  #сохраняем файл из переменной
        resulturl = rotatefunction('./pdf4/media/'+ file1name, grad1, pages1)   #вызываем функцию файла из pdf4.py, которая в файле file1name поворачивает страницы pages1 на градус из grad1, на выходе из которой получаем url для скачивания результата
        fs.delete(file1name)    #удаляем исходный файл
        return render(request, 'rotate.html', {
            'resulturl': resulturl
        })
    return render(request, 'rotate.html')

def in_pdf_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']  #передаем данные из формы в переменные
        file1name = fs.save(file1.name, file1)  #сохраняем файл из переменной
        resulturl = inpdffunction('./pdf4/media/'+ file1name)   #вызываем функцию для преобразования файла в PDF
        fs.delete(file1name)    #удаляем исходный файлы
        return render(request, 'in-pdf.html', {
            'resulturl': resulturl
        })
    return render(request, 'in-pdf.html')

def in_text_view(request):
    if request.method == 'POST' and request.FILES['file1']:
        fs = FileSystemStorage()        #создаем экземпляр джанго-класс для работы с файлами
        file1 = request.FILES['file1']  #передаем данные из формы в переменные
        format = request.POST['format1']
        file1name = fs.save(file1.name, file1)  #сохраняем файл из переменной
        resulturl = intextfunction('./pdf4/media/'+ file1name, format)   #вызываем функцию для преобразования файла в текстовый формат из pdf4.py, на выходе из которой получаем url для скачивания текстового файла
        fs.delete(file1name)    #удаляем исходный файлы
        return render(request, 'in-text.html', {
            'resulturl': resulturl
        })
    return render(request, 'in-text.html')

