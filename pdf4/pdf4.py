import PyPDF2
import random

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




