#smtplib是python内置模块，无需再次安装
import smtplib,base64, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# def send_email_smtp():
#     sender_email = base64.b64decode(b'ZnJhbmtfbGR3QDE2My5jb20=') # frank_ldw
#     receiver_email = base64.b64decode(b'Nzk4NDQ4NTAxQHFxLmNvbQ==') #798448501
#     password = base64.b64decode(b'xxxxxYmFRNDExNTP3Li4=')
#
#     # 创建邮件对象
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     message["Subject"] = "Test Send Email from smtplib"
#
#     # 邮件正文
#     boby = "This is a test mail sent from Python using smtplib"
#     message.attach(MIMEText(boby, "plain"))
#
#     try:
#         server = smtplib.SMTP("smtp.example.com", 587)
#         server.starttls()
#         server.login(sender_email, password)
#
#         # 发送邮件
#         server.sendmail(sender_email,receiver_email, message.as_string())
#         print("Send successfully")
#     except Exception as e:
#         print("Error" , e)
#     finally:
#         server.quit()
#
#
# send_email_smtp()
def __init__(self):
    # 初始化
    self.smtp = smtplib.SMTP()

    # 连接邮箱服务器地址
    self.smtp.connect('smtp.126.com')

    # 加入主题和附件，邮件体
    self.email_body = MIMEMultipart('mixed')

    # 发件人地址及授权码
    self.email_from_username = '**@126.com'
    self.email_from_password = '授权码'

    # 登录
    self.smtp.login(self.email_from_username, self.email_from_password)

def generate_email_body(self, email_to_list, email_title, email_content, attchment_path, files):
    """
    组成邮件体
    :param email_to_list:收件人列表
    :param email_title:邮件标题
    :param email_content:邮件正文内容
    :param attchment_path:附件的路径
    :param files:附件文件名列表
    :return:
    """
    self.email_body['Subject'] = email_title
    self.email_body['From'] = self.email_from_username
    self.email_body['To'] = ",".join(email_to_list)

    for file in files:
        file_path = attchment_path + '/' + file
        if os.path.isfile(file_path):
            # 构建一个附件对象
            att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            att.add_header("Content-Disposition", "attachment", filename=("gbk", "", file))
            self.email_body.attach(att)

    text_plain = MIMEText(email_content, 'plain', 'utf-8')
    self.email_body.attach(text_plain)


def exit(self):
    """
    退出服务
    :return:
    """
    self.smtp.quit()

