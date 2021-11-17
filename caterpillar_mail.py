import smtplib
from email.mime.text import MIMEText

class SendEmail(object):
    def __init__(self,send_mail_server):
        self.__smtp = smtplib.SMTP(send_mail_server, port=25)
        self.__From=""
        self.__To=""
        self.__password=""
        self.__subject=""
        self.__context=""
        self.__mail=None

    def __del__(self):
        try:
            self.__smtp.quit()
        except:
            pass

    @property
    def From(self):
        return self.__From

    @From.setter
    def From(self, From):
        self.__From = From

    @property
    def To(self):
        return self.__To

    @To.setter
    def To(self, To):
        self.__To = To

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self,pwd):
        self.__password=pwd

    @property
    def context(self):
        return self.__context

    @context.setter
    def context(self,ctx):
        self.__context=ctx

    @property
    def subject(self):
        return self.__subject

    @subject.setter
    def subject(self,subject):
        self.__subject=subject

    def send(self):
        self.__mail=MIMEText(self.__context)
        self.__mail["From"]=self.__From
        self.__mail["To"]=self.__To
        self.__mail["Subject"]=self.__subject
        self.__smtp.login(self.__From,self.__password)
        self.__smtp.sendmail(self.__From, self.__To, self.__mail.as_string())

class Send163Email(SendEmail):
    def __init__(self):
        super(Send163Email,self).__init__("smtp.163.com")