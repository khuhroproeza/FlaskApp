#1/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect
app = Flask(__name__)
from sqlcreater import showdata
import os
#from main import filedirect
inst = showdata()
posthome = (inst.showresult(All=True))
DictA, DictC, DictS, DictO,DictCOMB, DictBOHREN,DictConditioning,Performance,Powersave,TEP = inst.showresult(All=False)

filedirect = '/home/master/FlaskApp2'
def logintocondor():
    import pysftp
    import os
    global filedirect
    # os.chdir('/home/khuhro/l3S Projects/frameworkeditor')
    home = filedirect
    srv = pysftp.Connection(host="deken1.l3s.uni-hannover.de", username='khuhro', password='!trinity.DOT1'
                            )
    return srv

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posthome=DictCOMB)



def fileupdate():
    srv = logintocondor()
    global filedirect
    direct = filedirect
    direct = direct + '/savedresults2'
    os.chdir(direct)
    with srv.cd('/home/khuhro/FW2/savedresult'):
        condorlink = '/home/khuhro/FW2/savedresult'
        filecondor = (srv.listdir(condorlink))

        for i in filecondor:
            srv.get(condorlink+ '/' + i)
    srv.close()

@app.route("/seperate")
def seperate():
    fileupdate()
    return render_template('seperate.html', DictA =DictA , DictC = DictC, DictS=DictS , DictO = DictO)

@app.route("/ReadMe")
def ReadMe():
    return render_template(('ReadMe.html'))
'''
@app.route("/seperate2")
def seperate2():
    return render_template('seperate2.html',DictBOHREN =DictBOHREN, DictConditioning = DictConditioning,Performance=Performance,Powersave=Powersave,TEP=TEP)
'''

def filesync():
    srv = logintocondor()
    global filedirect
    home = filedirect

    with srv.cd('/home/khuhro/FW2/Datasets'):
        # chdir to public
        condorlink = '/home/khuhro/FW2/Datasets'
        filecondor = (srv.listdir(condorlink))
        filehome = os.listdir(home + '/uploads')

        # inter2 = [x for x in filecondor if x not in filehome]
        # print(inter2)
        # inter3 = [x for x in inter2 if x in filecondor]

        for i in filehome:
            print(i)
            remoter = home + '/' + 'uploads/' + i
            print(remoter)
            # sftp.get(remoter)
            # sftp.put(remoter)
            srv.put(remoter)  # upload file to nodejs/
    srv.close()

def filextensioncheck(name):
    _, extension = name.split('.')
    if extension != "csv":
        return False
    else:
        return True

#app.config["CSV_UPLOADS"] =
@app.route("/upload-file",methods=["GET","POST"])
def upload_file():
    global filedirect
    status = "PLEASE--UPLOAD--THE--FILE"
    if request.method == "POST":

       if request.files:

           print(filedirect)
           #filedirect1 = filedirect
           direct = filedirect
           direct = direct + '/uploads'


           file  = request.files["csv"]

           os.chdir(direct)
           name = str(file.filename)
           print(name, "HEREEEEEEEEEEEEEEEEEEEEE")
           checker = filextensioncheck(name)
           if checker == True:


               file.save(file.filename)
               #
               status = "FILE--UPLOADED!"
               filesync()
           else:
               status = 'File Extension Not Supported'


           redirect(request.url)


    return render_template("upload-file.html",status=status)

if __name__ == '__main__':
    app.run(host='iprod.l3s.uni-hannover.de', port='5000', debug=True)