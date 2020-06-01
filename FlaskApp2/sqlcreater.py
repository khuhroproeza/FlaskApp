#1/usr/bin/env python3
from main import filedirect
#filedirect = '/home/master/FlaskApp2'
class showdata:

    def __init__(self):

        pass

    from sklearn.externals import joblib
    def secondsToText(timer):
        timer = int(timer)
        days = timer// 86400
        hours = (timer - days * 86400) // 3600
        minutes = (timer - days * 86400 - hours * 3600) // 60
        seconds = timer - days * 86400 - hours * 3600 - minutes * 60
        seconds = int(seconds)
        result = ("{0} d{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
                 ("{0} hr{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
                 ("{0} m{1}, ".format(minutes, "" if minutes != 1 else "") if minutes else "") + \
                 ("{0} {1}, ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
        return result

    def showresult(self, Cname=None, Dname = None, All = False):
        global filedirect
        filedirect1 = filedirect
        #mycursor = mydb.cursor()

        def secondsToText(timer):
            days = timer// 86400
            hours = (timer - days * 86400) // 3600
            minutes = (timer - days * 86400 - hours * 3600) // 60
            seconds = timer - days * 86400 - hours * 3600 - minutes * 60
            seconds = int(seconds)
            result = ("{0} d{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
                    ("{0} hr{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
                    ("{0} m{1}, ".format(minutes, "" if minutes != 1 else "") if minutes else "") + \
                    ("{0} {1}, ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
            return result


        




        if All == True:

            pass
            
            
           
            
            #print(valuez)
            #print(finaldict)
            #for i in finaldict.keys():
                #print(finaldict[i][2])
            #finalalog = ['Parameters']
            #finaldict[0]
            
            #print(finalalog)
            #print(valuez)


        if All==False:
            def dictor(namelist,Name):
                dictnames = {}
                dictnames["Name"] = Name
                dictnames["True_Postive"] = int(namelist[0])
                dictnames["True_Negative"] = int(namelist[1])
                dictnames["False_Positive"] = int(namelist[2])
                dictnames["False_Negative"] = int(namelist[3])
                dictnames["Detection_Rate"] = "{0:.2f}".format(namelist[4])
                dictnames["False_Positive_Rate"] = "{0:.2f}".format(namelist[5])
                dictnames["Total_Time"] = secondsToText(namelist[6])
                dictnames["SD_Detection_Rate"] = "{0:.2f}".format(namelist[7])
                dictnames["SD_False_Alarm_rate"] = "{0:.2f}".format(namelist[8])
                return dictnames

                

            from sklearn.externals import joblib
            import os
            print(filedirect)
            filedirect1 = filedirect1
            direct = filedirect1
            print(direct, 'DataExtraction')
            direct = direct + '/savedresult'
            os.chdir(direct)
            datalist = list((os.listdir()))
            Datasets = []
            DatasetNames = []
            DictA= []
            DictC = []
            DictS = []
            DictO = []
            DictBOHREN = []
            DictConditioning = []
            Performance = []
            Powersave = []
            Frasen = []
            TEP = []
            DictCOMB = []



            for items in datalist:
                Name, _ = os.path.splitext(items)
                print(Name[-1])
                if Name[0]=='A':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    _, Name = Name.split('-')
                    DictA1 = dictor(listback,Name)
                    DictA.append(DictA1)


                elif Name[0]=='C':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    _, Name = Name.split('-')
                    DictA2 = dictor(listback,Name)
                    DictC.append(DictA2)
                elif Name[0]=='S':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    _, Name = Name.split('-')
                    DictA3 = dictor(listback,Name)
                    DictS.append(DictA3)
                elif Name[0]=='O':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    _, Name = Name.split('-')
                    DictA4 = dictor(listback,Name)
                    DictO.append(DictA4)

            for items in datalist:
                Name, _ = os.path.splitext(items)
                print(Name[-1])

                if Name[-2:]=='en':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    Name,_  = Name.split('-')
                    DictA5 = dictor(listback,Name)
                    DictBOHREN.append(DictA5)
                elif Name[-2:]=='ng':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    Name,_  = Name.split('-')
                    DictA6 = dictor(listback,Name)
                    DictConditioning.append(DictA6)
                elif Name[-2:]=='ce':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    print(listback, "trial of fasdfasdfasdfasdfasdfe")
                    Name, _ = os.path.splitext(items)
                    Name,_  = Name.split('-')
                    DictA7 = dictor(listback,Name)
                    Performance.append(DictA7)
                elif Name[-2:]=='ve':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    Name,_ = Name.split('-')
                    DictA8 = dictor(listback,Name)
                    Powersave.append(DictA8)
                    '''
                elif Name[-2:]=='en':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    Name,_ = Name.split('-')
                    DictA9 = dictor(listback,Name)
                    Frasen.append(DictA9)
                    '''
                elif Name[-2:]=='EP':
                    directoryname = direct + '/' + items
                    listback = joblib.load(directoryname)
                    Name, _ = os.path.splitext(items)
                    Name,_ = Name.split('-')
                    DictA9 = dictor(listback,Name)
                    TEP.append(DictA9)

            for items in datalist:
                Name, _ = os.path.splitext(items)
                

                
                directoryname = direct + '/' + items
                listback = joblib.load(directoryname)
                Name, _ = os.path.splitext(items)
                #Name,_  = Name.split('-')
                DictA0 = dictor(listback,Name)
                DictCOMB.append(DictA0)
            return DictA, DictC, DictS, DictO,DictCOMB, DictBOHREN,DictConditioning,Performance,Powersave,TEP #Frasen
