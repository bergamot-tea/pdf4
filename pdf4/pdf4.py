import PyPDF2
import random


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