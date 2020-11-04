import os, time

folder1 = './pdf4/media/pdfresult/'
folder2 = './pdf4/media/'

while True:
    for file in os.listdir(folder1):
        now=time.time()
        ctime = os.path.getctime(folder1 + file)
        delta = now - ctime
        if delta > 600:
            os.remove(folder1 + file)
    for file in os.listdir(folder2):
        if file != 'pdfresult':
            now=time.time()
            ctime = os.path.getctime(folder2 + file)
            delta = now - ctime
            if delta > 900:
                os.remove(folder2 + file)
    time.sleep(30)