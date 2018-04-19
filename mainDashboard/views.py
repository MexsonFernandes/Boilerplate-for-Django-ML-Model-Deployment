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
# Create your views here.

def index(request):
    if request.POST and request.FILES:
        try:###Assigning values to variables from post
            global filename, emailid,target, dir_name, id
            emailid = request.POST['emailid']
            filename = request.FILES['csv_file']

            target = request.POST['target']
            ###########################
            ####creating jobid from timestamp
            id = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            ####creating directory name for storing data
            dir_name = str(emailid) + "/" + str(id) + "/" + str(filename)
            ###saving to a file.
            path = default_storage.save(dir_name, ContentFile(filename.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)

            ###writing to  a log file.
            fp = open("media/" + str(emailid) + "/" + str(id) + "/" + str(id) + ".log", 'w')
            fp.write(str("\n\nFilename : " + str(filename) + "\nEmail id :" + str(
                emailid) + "\nID : " + str(id)))
            ####send message to user
            fp.close()
            subject = "File submitted successfully to RoboMex Server for processing!!!"
            message = "Hello Sir/Ma'am\n\nYour file has been successfully submitted to our server and is under processing mode. \n\nJob ID : " + str(
                id) + "\nFile Name : " + str(filename) + "\n\nRegards,\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(emailid)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)
            sendemail.send(fail_silently=False)
            runthread = ThreadingExample()
            return HttpResponseRedirect("/progress")
        except Exception as e:
            print(e)
            print(request.FILES)
            return HttpResponse("""<h3> There was some error in our system. We will rectify it and will let you know. In the mean time you can send an email to 8615208@apiit.edu.in if you urgently need to solve an issue.
                                    Thank you for using RoboMex Service.</h3>""")
    return render(request, 'index.html');

def progress(request):
    fp = open("media/" + str(emailid) + "/" + str(id) + "/" + str(id) + ".log", 'r')
    file=""
    refresh =True
    for i in fp:
        if i == "SUCCESSFULLY COMPLETED OPERATION":
            refresh = False
        file = "      "+ file +  "\n" + i + "\n"
    return render(request,"progress.html",{'file':file,'refresh':refresh})


class ThreadingExample(object):
    def __init__(self, interval =1 ):
        self.interval = interval
        runthread = threading.Thread(target = self.run,args=())
        runthread.daemon = True
        runthread.start()

    def run(self):
        done = 0
        thread_dir = "media/" + str(emailid) + "/" + str(id) + "/"
        distutils.dir_util.copy_tree('media/RScripts/', thread_dir)
        try:
            done = 1
            # print(os.getcwd())
            # os.chdir("MEDIA/" + str(email) + "/" + str(id) + "/")
            #mexson code best part starts here
            print(filename)
            command = "Rscript neuralNetwork.R " + str(filename) + " "+ str(target) + " >>"+str(id)+".log"
            os.system("(cd " + thread_dir + " && " + command + ")")
            # os.chdir(settings.BASE_DIR)
            #mexson code ends here
        except Exception as e:
            print(e)
            done = 0
            fp = open("media/" + str(emailid) + "/" + str(id) + "/" +str(id) +".log", 'a')
            fp.write("\nFAILURE IN SOME OPERATION")
            fp.close()
            subject = "Failure in DataSet " + str(filename) + " evaluation"
            message = "Hello Sir/Ma'am\n\nYour Job was not completed. Please check your dataset once again. You can send an email to 8615208@apiit.edu.in for clarification.\n\nJOB ID : " + str(
                id) + " Failed\n\nRegards,\nAdmin\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(emailid)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)
            fd = open(str("media/" + str(emailid) + "/" + str(id) + "/" + str(id+".log")), 'r')
            sendemail.attach(str(id) + ".log", fd.read(), 'text/plain')
            sendemail.send()
            fd.close()
        if done == 1:
            fp = open("media/" + str(emailid) + "/" + str(id) + "/"+ str(id) + ".log", 'a')
            fp.write("\nSUCCESSFULLY COMPLETED OPERATION")
            fp.close()
            subject = "Successfully completed DataSet " + str(filename) + " evaluation"
            message = "Hello Sir/Ma'am\n\nYour Job was successfully completed. Please check your result in the file attached.\n\n\nJOB ID : " + str(
                id) + " COMPLETED\n\nRegards,\nAdmin\nMexson Fernandes"
            from_email = settings.EMAIL_HOST_USER
            to_list = [str(emailid)]
            sendemail = EmailMessage(str(subject), str(message), str(from_email), to_list)

            log = open(str("media/" + str(emailid) + "/" + str(id) + "/" + str(id + ".log")), 'r')
            sendemail.attach(str(id) + ".log", log.read(), 'text/plain')

            AP = open(str("media/" + str(emailid) + "/" + str(id) + "/" + "neuralNetwork-ActualPredicted-Result.csv"), 'r')
            sendemail.attach("neuralNetwork-ActualPredicted-Result.csv",AP.read(),'text/plain')

            Result = open(str("media/" + str(emailid) + "/" + str(id) + "/" + "neuralNetwork-Evaluation-Result.csv"), 'r')
            sendemail.attach("neuralNetwork-Evaluation-Result.csv", Result.read(), 'text/plain')

            ModelBuild =  open(str("media/" + str(emailid) + "/" + str(id) + "/" + "neuralNetwork-Model.RData"), 'r')
            sendemail.attach("neuralNetwork-Model.RData", ModelBuild.read(), 'text/plain')

            plot =open(str("media/" + str(emailid) + "/" + str(id) + "/" + "neuralNetwork-ScatterPlot.png"), 'r')
            sendemail.attach("neuralNetwork-ScatterPlot.png", plot.read(), 'text/plain')

            sendemail.send()
            AP.close()
            log.close()
            plot.close()
            ModelBuild.close()
            Result.close()