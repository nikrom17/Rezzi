#!/usr/bin/python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import email
import email.mime.application

name = "Adam Klein"
resume_filepath = "../pdf_generator/resume.pdf"

def createMessage():
    message = MIMEMultipart()
    message['From'] = user
    message['To'] = ", ".join(friends)
    message['Subject'] = name + "'s Resume for Review & Printing"
    return (message)

def addPDF():
    fp=open(resume_filepath,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename='resume.pdf')
    message.attach(att)

def addBodyText(message):
    body_html = '''<html><p style="color:grey;">\
    Hi. Rezzi Here, \n  %s just finished their resume\
    and is looking to get it reviewed as well as printed.\
    You can expect a visit from him soon!</p></html>''' % name
    message.attach(MIMEText(body_html,'html'))

def sendEmail(message, user, password, friends, images):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.connect('smtp.gmail.com', 587)
        server.starttls()
        server.login(user, password)
        server.send_message(message)
        server.quit()
    except SMTPException:
       print ("😭 Error: unable to send job email 😭")

if __name__ == "__main__":
    user  = 'joenotabot@gmail.com'
    password = 'joejoejoejoe'
    friends = ['bethnenniger@gmail.com']
    images = ['images/temp.gif']
    
    message = createMessage()
    createMessage()
    addPDF()
    addBodyText(message)
    sendEmail(message, user, password, friends, images)
