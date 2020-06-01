def dataretrieve():
    #filedirect = '/home/khuhroproeza/l3S Projects/flaskapp/FlaskApp2'
    filedirect = '/home/khuhroproeza/FrameWork'
    import joblib

    import os
    #direct = filedirect + '/savedresults'
    direct = filedirect + '/trial'
    os.chdir(direct)
    datalist = list((os.listdir(direct)))
    Alg = []
    Datasets = []
    for items in datalist:
        Name, _ = os.path.splitext(items)
        AL, DS = Name.split('-')
        Alg.append(AL)
        Datasets.append(DS)
    Alg = list(set(Alg))
    Alg.sort()
    Datasets = list(set(Datasets))
    Datasets.sort()

    def secondsToText(timer):
        timer = int(timer)
        days = timer // 86400
        hours = (timer - days * 86400) // 3600
        minutes = (timer - days * 86400 - hours * 3600) // 60
        seconds = timer - days * 86400 - hours * 3600 - minutes * 60
        seconds = int(seconds)
        result = ("{0} d{1}, ".format(days, "s" if days != 1 else "") if days else "") + \
                 ("{0} hr{1}, ".format(hours, "s" if hours != 1 else "") if hours else "") + \
                 ("{0} m{1}, ".format(minutes, "" if minutes != 1 else "") if minutes else "") + \
                 ("{0} {1}, ".format(seconds, "s" if seconds != 1 else "") if seconds else "")
        return result

    def dictor(namelist, Name):

        dictnames = {}
        dictnames["Name"] = Name
        dictnames["True_Postive"] = int(namelist[0])
        dictnames["True_Negative"] = int(namelist[1])
        dictnames["False_Positive"] = int(namelist[2])
        dictnames["False_Negative"] = int(namelist[3])
        dictnames["Detection_Rate"] = "{0:.2f}".format(namelist[4])
        dictnames["False_Positive_Rate"] = "{0:.2f}".format(namelist[5])
        dictnames["Total_Time"] = secondsToText(namelist[6])
        dictnames["SD_Detection_Rate"] = "{0:.2f}".format(namelist[8])
        dictnames["SD_False_Alarm_rate"] = "{0:.2f}".format(namelist[9])
        dictnames["AUC"] = "{0:.2f}".format(namelist[7])
        return dictnames

    Alge = {}
    for i in Alg:
        Alge["{0}".format(i)] = {}
        for e in Datasets:
            Name = i + '-' + e + '.pkl'
            if Name in datalist:
                Name = direct + '/' + Name
                listback = joblib.load(Name)
                Alge["{0}".format(i)]['{0}'.format(e)] = dictor(listback, e)
    Dsets = {}
    for i in Datasets:
        Dsets["{0}".format(i)] = {}
        for e in Alg:
            Name = e + '-' + i + '.pkl'
            if Name in datalist:
                Name = direct + '/' + Name
                listback = joblib.load(Name)
                Dsets["{0}".format(i)]['{0}'.format(e)] = dictor(listback, e)
    combined = {}
    for i in datalist:
        Name = direct + '/' + i
        listback = joblib.load(Name)
        classifer, _ = i.split('.')
        combined["{0}".format(classifer)] = dictor(listback, classifer)

    return Dsets, Alge, combined

