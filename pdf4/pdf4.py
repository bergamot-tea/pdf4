import PyPDF2
import random
import zipfile
import img2pdf
from pdf2image import convert_from_path
from django.core.files.storage import FileSystemStorage
from pdfrw import PdfReader, PdfWriter

#функция объединяет два PDF-файла и выдает ссылку на результирующий файл
def mergefunction(f1,f2):
    file1 = open(f1,'rb')
    file2 = open(f2,'rb')
    merger = PyPDF2.PdfFileMerger()
    merger.append(fileobj=file1)
    merger.append(fileobj=file2)
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    url1 = './pdf4/media/pdfresult/' + psw + '.pdf'
    merger.write(open(url1,'wb'))
    url2 = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.pdf'
    file1.close()
    file2.close()
    merger.close()
    return url2

#функция возвращает количество страниц PDF-файла
def getnumpagesfunction(f1):
    file1 = open(f1,'rb')
    pdf1 = PyPDF2.PdfFileReader()
    numpages = pdf1.getNumPages()
    file1.close()
    pdf1.close()
    return numpages


#функция вставляет второй PDF-файл в первый после страницы S первого файла
def insertfunction(f1,f2,s):
    file1 = open(f1,'rb')
    file2 = open(f2,'rb')
    merger = PyPDF2.PdfFileMerger()
    merger.merge(position=0, fileobj=file1)
    merger.merge(position = s, fileobj=file2)
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    url1 = './pdf4/media/pdfresult/' + psw + '.pdf'
    merger.write(open(url1,'wb'))
    url2 = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.pdf'
    file1.close()
    file2.close()
    merger.close()
    return url2

#функция разделяет PDF-файл на страницы и сохраняет их в архив
def split1function(f1):
    url = ''
    fs = FileSystemStorage(location='./pdf4/media/') #если не указать location то файлы в цикле почему то не удаляются
    file1 = open(f1,'rb')
    reader1 = PyPDF2.PdfFileReader(file1)
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
    url = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.zip'
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
    reader1 = PyPDF2.PdfFileReader(file1)
    numpages = reader1.getNumPages()    #в этой функции numpages нам нужна только для того чтоб мы могли циклом по файлам пройтись
    psw = '' # предварительно создаем переменную psw
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    zip1 = zipfile.ZipFile('./pdf4/media/pdfresult/' + psw + '.zip', 'w')   #создаем архив
    convert_from_path(f1, output_folder='./pdf4/media/', fmt=format, output_file=psw,)  #делаем из pdf картинки
    for i in range(numpages):
        zip1.write('./pdf4/media/' + psw + '0001-' + str(i + 1) + dotformat, arcname = str(i + 1) + dotformat) #записываем файл со страницей в архив, если не указать arcname то в архив попадет структура каталогов
        fs.delete(psw + '0001-' + str(i + 1) + dotformat) #удаляем незаархивированные картинки
    file1.close()
    zip1.close()
    url = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.zip'
    return url

#функция преобразует файлы изображений в один PDF-файл, вернее всначала преобразует их в отдельные pdf-файлы, затем объединяет их
def outimagesfunction(f1,f2,f3,f4,f5):   #тут filenames это список образованный из ключей словаря

    psw = ''
    for x in range(12):
        psw = psw + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnm'))
    fs = FileSystemStorage(location='./pdf4/media/')    #это чтоб в конце цикла мы смогли временные файлы удалить
    imgs = [f1,f2,f3,f4,f5] #словарь для прохода по циклу
    i = 0 #счетчик для цикла, в цикле номер страницы результирующего файла
    writer = PdfWriter()    #создаем writer для работы с pdfrw, чтоб после цикла записать результат
    for name in imgs:       #проходим по словарю imgs
        if name != None:    #если элемент словаря не имеет значене None (если пользвотаель загрузил файл)
            i = i + 1       #номер страницы результирующего файла (1,2,3...)
            name = './pdf4/media/' + name   #необходимо так как мы из вьюшки передали имена без './pdf4/media/'
            temppdf = './pdf4/media/' + str(i) + '_' + psw + '.pdf' #переменная имени отдельного pdf-файла для каждой страницы
            pdf1 = open(temppdf,'wb')   #открываем (создаем) на запись файл с именем из переменной temppdf
            pdf1.write(img2pdf.convert(name))   #записываем в него картинку
            pdf1.close()    #закрываем его
            #до этого момента в цикле работали с модульем img2pdf, далее pdfrw
            page = PdfReader(temppdf, decompress=False).pages   #записываем в page страницу из файла temppdf
            writer.addpages(page)   #добавляем во writer страницу page
            fs.delete(str(i) + '_' + psw + '.pdf')  #удаляем временные pdf-файлы
    writer.write('./pdf4/media/pdfresult/' + psw + '.pdf')  #записываем writer в файл
    url = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.pdf'
    return url






