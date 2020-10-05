# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import threading

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
import multiprocessing
from django.http import HttpResponse, HttpResponseRedirect
import subprocess
import distutils.dir_util
from django.conf import settings
import os, datetime

from django.core.mail import send_mail
from django.core.mail import EmailMessage

email = ''
id = ''

def index(request):
    if request.POST and request.FILES:
        try:###Assigning values to variables from post
            global email, id
            email = request.POST['emailid']
            file = request.FILES['csv_file']

            target = request.POST['target']
            ###########################
            ####creating jobid from timestamp
            id = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            ####creating directory name for storing data
            dir_name = str(email) + "/" + str(id) + "/" + str(file.name)
            ###saving to a file.
            path = default_storage.save(dir_name, ContentFile(file.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            ###writing to  a log file.
            fp = open("media/" + str(email) + "/" + str(id) + "/" + str(id) + ".log", 'w')
            fp.write(str("\n\nFilename : " + str(file.name) + "\nEmail id :" + str(
                email) + "\nID : " + str(id)))
            ####send message to user
            fp.close()
            subject = "File submitted successfully to RoboMex Server for processing!!!"
            message = "Hello Sir/Ma'am\n\nYour file has been successfully submitted to our server and is under processing mode. \n\nJob ID : " + str(
                id) + "\nFile Name : " + str(file.name) + "\n\nRegards,\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(email)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)
            sendemail.send(fail_silently=False)
            runthread = ThreadingExample(email, file.name, target, id)
            return HttpResponseRedirect("/progress")
        except Exception as e:
            print(e)
            print(request.FILES)
            return HttpResponse("""<h3> There was some error in our system. We will rectify it and will let you know. In the mean time you can send an email to 8615208@apiit.edu.in if you urgently need to solve an issue.
                                    Thank you for using RoboMex Service.</h3>""")
    return render(request, 'index.html');

def progress(request):
    global email, id
    fp = open("media/" + str(email) + "/" + str(id) + "/" + str(id) + ".log", 'r')
    file=""
    refresh =True
    for i in fp:
        if i == "SUCCESSFULLY COMPLETED OPERATION":
            refresh = False
        file = "      "+ file +  "\n" + i + "\n"
    return render(request,"progress.html",{'file':file,'refresh':refresh})


class ThreadingExample(object):
    def __init__(self, email, filename, target, id, interval =1 ):
        self.interval = interval
        self.email = email
        self.filename = ''.join(filename)
        self.target = target
        self.id = id
        runthread = threading.Thread(target = self.run,args=())
        runthread.daemon = True
        runthread.start()

    def run(self):
        done = 0
        thread_dir = "media/" + str(self.email) + "/" + str(self.id) + "/"
        distutils.dir_util.copy_tree('media/RScripts/', thread_dir)
        try:
            done = 1
            # print(os.getcwd())
            # os.chdir("MEDIA/" + str(email) + "/" + str(self.id) + "/")
            #mexson code best part starts here
            command = "Rscript neuralNetwork.R " + str(self.filename) + " "+ str(self.target) + " >>"+str(self.id)+".log"
            print(thread_dir)
            print(command)
            os.system("(cd " + thread_dir + " && " + command + ")")
            # os.chdir(settings.BASE_DIR)
            # mexson bad code ends here
        except Exception as e:
            print(e)
            done = 0
            fp = open("media/" + str(self.email) + "/" + str(self.id) + "/" +str(self.id) +".log", 'a')
            fp.write("\nFAILURE IN SOME OPERATION")
            fp.close()
            subject = "Failure in DataSet " + str(self.filename) + " evaluation"
            message = "Hello Sir/Ma'am\n\nYour Job was not completed. Please check your dataset once again. You can send an email to 8615208@apiit.edu.in for clarification.\n\nJOB ID : " + str(
                self.id) + " Failed\n\nRegards,\nAdmin\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(self.email)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)
            fd = open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + str(self.id+".log")), 'r')
            sendemail.attach(str(self.id) + ".log", fd.read(), 'text/plain')
            sendemail.send()
            fd.close()
        if done == 1:
            fp = open("media/" + str(self.email) + "/" + str(self.id) + "/"+ str(self.id) + ".log", 'a')
            fp.write("\nSUCCESSFULLY COMPLETED OPERATION")
            fp.close()
            subject = "Successfully completed DataSet " + str(self.filename) + " evaluation"
            message = "Hello Sir/Ma'am\n\nYour Job was successfully completed. Please check your result in the file attached.\n\n\nJOB ID : " + str(
                self.id) + " COMPLETED\n\nRegards,\nAdmin\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(self.email)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)

            log = open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + str(self.id + ".log")), 'r')
            sendemail.attach(str(self.id) + ".log", log.read(), 'text/plain')

            AP = open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + "neuralNetwork-ActualPredicted-Result.csv"), 'r')
            sendemail.attach("neuralNetwork-ActualPredicted-Result.csv",AP.read(),'text/plain')

            Result = open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + "neuralNetwork-Evaluation-Result.csv"), 'r')
            sendemail.attach("neuralNetwork-Evaluation-Result.csv", Result.read(), 'text/plain')
            
            with open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + "neuralNetwork-Model.RData"), 'r', encoding='utf-8', errors='ignore') as model:
                sendemail.attach("neuralNetwork-Model.RData", model.read(), 'text/plain')
            
            with open(str("media/" + str(self.email) + "/" + str(self.id) + "/" + "neuralNetwork-ScatterPlot.png"), 'r', encoding='utf-8', errors='ignore') as image:
                sendemail.attach("neuralNetwork-ScatterPlot.png", image.read())

            sendemail.send()
            AP.close()
            log.close()
            Result.close()