import PyPDF2
import random
import zipfile
from django.core.files.storage import FileSystemStorage

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
        file2 = open(name, 'wb')    #создаем файл для страницы
        writer1.write(file2)    #записываем в файл страницу
        file2.close() #закрываем файл
        zip1.write(name, arcname = str(i + 1) + '.pdf') #записываем файл со страницей в архив, если не указать arcname то в архив попадет структура каталогов
        fs.delete(str(i + 1) + '_' + psw + '.pdf')  #удаляем файл
    file1.close()
    zip1.close()
    url = 'http://pdf4.pythonanywhere.com/media/pdfresult/' + psw + '.zip'
    return url







