from smtplib import SMTP_SSL as SMTP
import logging
import logging.handlers
import sys
from email.mime.text import MIMEText
import os,time
from unit.getEnv import getEnv

class sendMail:
    def __init__(self, mailSubjectName, mailMessage, mailList):
        super().__init__();
        text = mailMessage

        msg = MIMEText(text, 'plain')
        msg['Subject'] = mailSubjectName; 
        self.me = getEnv("mailAddr").getEnv() 
        self.To = mailList
#        print(self.To)
        self.msg = msg

    def send_confirmation(self,):
        try:
            conn = SMTP('smtp.163.com')
#            conn.set_debuglevel(True)
#            print(getEnv("mailAddr").getEnv(), getEnv("mailPW").getEnv())
            conn.login(getEnv("mailAddr").getEnv(), getEnv("mailPW").getEnv())

            if len(self.To) > 0:
               try:
                    for i in range(0, len(self.To)):
                        conn.sendmail(self.me, self.To[i], self.msg.as_string())
                        time.sleep(5)
               finally:
                    conn.close()

        except Exception as exc:
            self.logger.error("ERROR!!!")
            self.logger.critical(exc)
            sys.exit("Mail failed: {}".format(exc))


    def sendmail(self,):
        logger = logging.getLogger(__name__)
        self.logger = logger
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        random_ass_condition = True

        if random_ass_condition:
            self.send_confirmation()

#if __name__ == "__main__":
#    sendmail = sendMail("eeeeeeee", "TTTTTTTTTT", '378153740@qq.com')
#    sendmail.sendmail();
#    sendmail.sendmail();
