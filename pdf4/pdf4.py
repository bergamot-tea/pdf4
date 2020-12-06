import PyPDF2
import random
import zipfile
import img2pdf
import os
from pdf2image import convert_from_path
from django.core.files.storage import FileSystemStorage
from pdfrw import PdfReader, PdfWriter
from PIL import Image

#функция объединяет два PDF-файла и выдает ссылку на результирующий файл
def mergefunction(f1,f2):
    file1 = open(f1,'rb')
    file2 = open(f2,'rb')
    merger = PyPDF2.PdfFileMerger(strict = False) # strict = False исправляет ошибку "Expected object ID (8 0) does not match actual (7 0); xref table not zero-indexed."
    merger.append(fileobj=file1)
    merger.append(fileobj=file2)
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    url1 = './pdf4/media/pdfresult/' + psw + '.pdf'
    merger.write(open(url1,'wb'))
    url2 = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    file1.close()
    file2.close()
    merger.close()
    return url2

#функция возвращает количество страниц PDF-файла
def getnumpagesfunction(f1):
    file1 = open(f1,'rb')
    pdf1 = PyPDF2.PdfFileReader(file1,strict = False)
    numpages = pdf1.getNumPages()
    file1.close()
    pdf1.close()
    return numpages


#функция вставляет второй PDF-файл в первый после страницы S первого файла
def insertfunction(f1,f2,s):
    file1 = open(f1,'rb')
    file2 = open(f2,'rb')
    merger = PyPDF2.PdfFileMerger(strict = False)
    merger.merge(position=0, fileobj=file1)
    merger.merge(position = s, fileobj=file2)
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    url1 = './pdf4/media/pdfresult/' + psw + '.pdf'
    merger.write(open(url1,'wb'))
    url2 = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    file1.close()
    file2.close()
    merger.close()
    return url2

#функция разделяет PDF-файл на страницы и сохраняет их в архив
def split1function(f1):
    url = ''
    fs = FileSystemStorage(location='./pdf4/media/') #если не указать location то файлы в цикле почему то не удаляются
    file1 = open(f1,'rb')
    reader1 = PyPDF2.PdfFileReader(file1, strict = False)   # strict = False исправляет ошибку "Expected object ID (8 0) does not match actual (7 0); xref table not zero-indexed."
    numpages = reader1.getNumPages()
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    zip1 = zipfile.ZipFile('./pdf4/media/pdfresult/' + psw + '.zip', 'w')   #создаем архив
    for i in range(numpages):
        writer1 = PyPDF2.PdfFileWriter() #создаем экземпляр класса для записи
        page = reader1.getPage(i)   #достаем страницу
        writer1.addPage(page)   #крепим страницу к экземпляру класса
        name = './pdf4/media/' + str(i + 1) + '_' + psw + '.pdf'
        file2 = open(name, 'wb')    #создаем файл для страницы (он пока что не в архиве)
        writer1.write(file2)    #записываем в файл страницу
        file2.close() #закрываем файл
        zip1.write(name, arcname = str(i + 1) + '.pdf') #записываем файл со страницей в архив, если не указать arcname то в архив попадет структура каталогов
        fs.delete(str(i + 1) + '_' + psw + '.pdf')  #удаляем файл
    file1.close()
    zip1.close()
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.zip'
    return url

#функция преобразует PDF-файл в архив с изображениям
def inimagesfunction(f1, format):

    if format == 'jpeg':
        dotformat = '.jpg'
    elif format == 'png':
        dotformat = '.png'
    elif format == 'tiff':
        dotformat = '.tif'
    else:
        dotformat = '.ppm'

    url = ''
    fs = FileSystemStorage(location='./pdf4/media/') #если не указать location то файлы в цикле почему то не удаляются
    file1 = open(f1,'rb')
    reader1 = PyPDF2.PdfFileReader(file1, strict = False)
    numpages = reader1.getNumPages()    #в этой функции numpages нам нужна только для того чтоб мы могли циклом по файлам пройтись
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    zip1 = zipfile.ZipFile('./pdf4/media/pdfresult/' + psw + '.zip', 'w')   #создаем архив
    convert_from_path(f1, output_folder='./pdf4/media/', fmt=format, output_file=psw,)  #делаем из pdf картинки
    for i in range(numpages):
        if i<9:
            zip1.write('./pdf4/media/' + psw + '0001-0' + str(i + 1) + dotformat, arcname = str(i + 1) + dotformat) #записываем файл со страницей в архив, если не указать arcname то в архив попадет структура каталогов
        else:
            zip1.write('./pdf4/media/' + psw + '0001-' + str(i + 1) + dotformat, arcname = str(i + 1) + dotformat) #разница в том что меньше десяти файлы создаются 01 02... а далее 10 11 12
        fs.delete(psw + '0001-' + str(i + 1) + dotformat) #удаляем незаархивированные картинки
    file1.close()
    zip1.close()
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.zip'
    return url

#функция преобразует файлы изображений в один PDF-файл, вернее всначала преобразует их в отдельные pdf-файлы, затем объединяет их
def outimagesfunction(f1,f2,f3,f4,f5):   #тут filenames это список образованный из ключей словаря

    psw = ''
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    fs = FileSystemStorage(location='./pdf4/media/')    #это чтоб в конце цикла мы смогли временные файлы удалить
    imgs = [f1,f2,f3,f4,f5] #список для прохода по циклу
    i = 0 #счетчик для цикла, в цикле номер страницы результирующего файла
    writer = PdfWriter()    #создаем writer для работы с pdfrw, чтоб после цикла записать результат
    for name in imgs:       #проходим по списку imgs
        if name != None:    #если элемент словаря не имеет значене None (если пользвотаель загрузил файл)
            i = i + 1       #номер страницы результирующего файла (1,2,3...)
            name = './pdf4/media/' + name   #необходимо так как мы из вьюшки передали имена без './pdf4/media/'
            temppdf = './pdf4/media/' + str(i) + '_' + psw + '.pdf' #переменная имени отдельного pdf-файла для каждой страницы
            pdf1 = open(temppdf,'wb')   #открываем (создаем) на запись файл с именем из переменной temppdf

            im = Image.open(name)
            if ('A' in im.getbands()) or ('a' in im.getbands()):    #убираем альфа-канал если есть
                im.convert('RGB').save(name)

            pdf1.write(img2pdf.convert(name))   #записываем в него картинку
            pdf1.close()    #закрываем его
            #до этого момента в цикле работали с модульем img2pdf, далее pdfrw
            page = PdfReader(temppdf, decompress=False).pages   #записываем в page страницу из файла temppdf
            writer.addpages(page)   #добавляем во writer страницу page
            fs.delete(str(i) + '_' + psw + '.pdf')  #удаляем временные pdf-файлы
    writer.write('./pdf4/media/pdfresult/' + psw + '.pdf')  #записываем writer в файл
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    return url

#функция сжимает pdf-файл f1 со степенью сжатия level
def compressfunction(f1, level):

    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    #    cmd = 'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook -dNOPAUSE -dQUIET -dBATCH -sOutputFile=./media/222.pdf ./media/333.pdf'
    cmd = 'gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/' + level + ' -dNOPAUSE -dQUIET -dBATCH -sOutputFile=./pdf4/media/pdfresult/' + psw + '.pdf ' + f1
    os.system(cmd)
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    return url



#функция берет файл f1, поворачивает страницы из pages1 на градус grad1, записывает все это дело в новый файл и возвращает ссылку на новый файл. При этом pages1 - строка введенная пользователем.
def rotatefunction(f1, grad1, pages1):

    reader = PyPDF2.PdfFileReader(f1, strict = False)
    writer = PyPDF2.PdfFileWriter()
    numpages = reader.getNumPages()    #количество страниц файла (нужно для цикла)

    pages = pages1.split(',')

    digits = [] #список для интовых значений страниц

    ### в этом цикле разбираем пользовательский ввод на список страниц
    for i in pages:     # тут i строки состоящие из цифр например '5' или из диапазонов например '3-8'
        if i.isnumeric() == True:
            digits.append(int(i))   #добавляем в список digits элемент i
        else:
            r = i.split('-')    #вытаскиваем из диапазонов '3-8' начало и конец диапазона и помещаем в список r
            for a in range(int(r[0]),int(r[1])+1):  #проходимся по диапазону и помещаем в список digits все числа из диапазона
                digits.append(a)

    ### если номер страницы входит в digits то добавляем повернутую страницу на grad1 градусов в объект writer, если нет то добавляем не повернутую
    for n in range(numpages):
        if n + 1 in digits:
            p1 = reader.getPage(n).rotateClockwise(int(grad1))
            writer.addPage(p1)
        else:
            p1 = reader.getPage(n)
            writer.addPage(p1)


    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    name = './pdf4/media/pdfresult/' + psw + '.pdf'
    file1 = open(name, 'wb')
    writer.write(file1)     #записываем все страницы из объекта writer в файл name

    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    return url





def inpdffunction(f1):

    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    cmd = 'abiword --to=pdf --to-name=./pdf4/media/pdfresult/' + psw + '.pdf ' + f1
    os.system(cmd)  #тут вызываем консольную команду
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.pdf'
    return url




def intextfunction(f1, format):

    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    cmd = 'abiword --to=' + format + ' --to-name=./pdf4/media/pdfresult/' + psw + '.' + format + ' ' + f1
    os.system(cmd)  #тут вызываем консольную команду
    url = 'https://pdf4you.ru/media/pdfresult/' + psw + '.' + format
    return url



