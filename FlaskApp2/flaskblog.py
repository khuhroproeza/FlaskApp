#1/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect

from sqldata import dataretrieve
import pandas as pd
app = Flask(__name__)
#from sqlcreater import showdata
import os
#from main import filedirect
#inst = showdata()
#posthome = (inst.showresult(All=True))
def dataextract():
    dsets, alge, combined = dataretrieve()
    return  dsets, alge,combined

#filedirect = '/home/master/FlaskApp2'
filedirect = '/home/khuhroproeza/l3S Projects/flaskapp/FlaskApp2'
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
    _,_,combined = dataextract()
    return render_template('home.html', posthome=combined)

#Appends the CSV file to check the status
def jobscounter(stdout, filename):
    filename, _ = filename.split('.')
    _, statement = stdout
    global filedirect

    file = filedirect + '/status.csv'
    data = pd.read_csv(file)

    FindFirst = data.index[data['Name'] == filename].tolist()
    if len(FindFirst) == 0:
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        statement = statement[-6:-2]
        status = 'Pending'
        entry = {'Name': [filename], 'Job Id': [statement], 'Status': [status], 'Date': [dt_string]}
        dpd = pd.DataFrame(entry)

        final = pd.concat([data, dpd])

        final.to_csv(file, index=False)


#Function to submit the files to condor


def serversubmit(filename):
    import paramiko
    from paramiko import client
    ssh = paramiko.SSHClient()
    host = 'deken1.l3s.uni-hannover.de'
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='khuhro', password='!trinity.DOT1')
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('condor_submit serverrunner.submit')
    stdout=ssh_stdout.readlines()
    jobscounter(stdout,filename)
    print('DONE')

#To load readme files for Readme Page
def readmepage():
    global filedirect
    fileloc = filedirect + '/readmefiles'
    import os

    os.chdir(fileloc)
    datalist = list((os.listdir()))
    readmedict = {}
    for i in datalist:
        fname, _ = i.split('.')
        namefile = fileloc + '/' + i

        print(fname)
        f = open(namefile, "r")
        if f.mode == 'r':
            contents = f.read()
            readmedict["{0}".format(fname)] = [contents[:-1]]
    return readmedict

def fileupdate():
    srv = logintocondor()
    global filedirect
    direct = filedirect
    #direct = direct + '/savedresults'
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
    #fileupdate()
    dsets, alge,_ = dataextract()
    return render_template('seperate.html', DictA =alge)

@app.route("/ReadMe")
def ReadMe():
    datadict = readmepage()
    return render_template('ReadMe.html', datadict = datadict)

@app.route("/seperate2")
def seperate2():
    dsets, alge,_ = dataextract()
    return render_template('seperate2.html',DictA=dsets)

#Status updater
def statuscheck():
    global filedirect
    file = filedirect + '/status.csv'
    DF = pd.read_csv(file)
    for row in DF.iterrows():
        job = (row[1][1])
        command = 'condor_q -better-analyze' + ' ' + str(job)
        import paramiko
        from paramiko import client
        ssh = paramiko.SSHClient()
        host = 'deken1.l3s.uni-hannover.de'
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username='khuhro', password='!trinity.DOT1')
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
        stdout=ssh_stdout.readlines()
        if len(stdout)<15:

            DF.iloc[row[0],2] = 'DONE'
    DF.to_csv(file,index=False)
    backdata = {}
    for row in DF.iterrows():
        backdata[row[1][0]] = [row[1][1],row[1][2],row[1][3]]
    return backdata

#TO create README from uplaod function
def readmecreater(ft, text):
    print(ft, "HERE @@@")
    filename, _ = ft.split('.')
    global filedirect
    fileloc = filedirect + '/readmefiles'
    import os

    os.chdir(fileloc)
    datalist = list((os.listdir()))
    print(datalist, "data lister")
    for i in range(len(datalist)):
        name, _ = datalist[i].split('.')
        datalist[i] = name
    if filename not in datalist:
        filename = filename + '.txt'
        f = open(filename, "w+")
        f.write(text)
        f.close()
        return True
    else:
        return False
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

       if request.files and request.form:

           print(filedirect)
           #filedirect1 = filedirect
           direct = filedirect
           direct = direct + '/uploads'


           file  = request.files["csv"]
           description = request.form["textfield"]
           print(description)

           os.chdir(direct)
           name = str(file.filename)
           print(name, "HEREEEEEEEEEEEEEEEEEEEEE")
           checker = filextensioncheck(name)
           if checker == True:


               file.save(file.filename)
               print(name, "HERE T")
               Respon = readmecreater(name,description)
               if Respon == True:
                   filesync()
                   serversubmit(name)
                   status = "FILE--UPLOADED--&--sent!"
               else:
                   status = "File--Already--Exists"
           else:
               status = 'File--Extension--Not--Supported'


           redirect(request.url)

    checker = statuscheck()
    return render_template("upload-file.html",status=status, checker=checker)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
    #app.run(host='iprod.l3s.uni-hannover.de', port = '5000', debug=True)

