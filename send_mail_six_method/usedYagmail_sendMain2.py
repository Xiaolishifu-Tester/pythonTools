import yagmail

# 连接服务器
# 用户名、授权码、服务器地址
yag_server = yagmail.SMTP(user='**@126.com', password='授权码', host='smtp.126.com')
# 发送对象列表
email_to = ['**@qq.com', ]
email_title = '测试报告'
email_content = "这是测试报告的具体内容"
# 附件列表
email_attachments = ['./attachments/report.png', ]

# 发送邮件
yag_server.send(email_to, email_title, email_content, email_attachments)
# 关闭连接
yag_server.close()
