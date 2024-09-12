#smtplib是python内置模块，无需再次安装
import smtplib,base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_smtp():
    sender_email = base64.b64decode(b'ZnJhbmtfbGR3QDE2My5jb20=') # frank_ldw
    receiver_email = base64.b64decode(b'Nzk4NDQ4NTAxQHFxLmNvbQ==') #798448501
    password = base64.b64decode(b'dGFvYmFvNDExNTI3Li4=')

    # 创建邮件对象
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Test Send Email from smtplib"

    # 邮件正文
    boby = "This is a test mail sent from Python using smtplib"
    message.attach(MIMEText(boby, "plain"))

    try:
        server = smtplib.SMTP("smtp.example.com", 587)
        server.starttls()
        server.login(sender_email, password)

        # 发送邮件
        server.sendmail(sender_email,receiver_email, message.as_string())
        print("Send successfully")
    except Exception as e:
        print("Error" , e)
    finally:
        server.quit()


send_email_smtp()