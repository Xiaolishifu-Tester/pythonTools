import yagmail

def send_email_yagmail():
    sender_email = "your_email@example.com"
    password = "your_password"
    receiver_email = "receiver_email@example.com"

    yag = yagmail.SMTP(user=sender_email, password=password)
    subject = "Test Email from yagmail"
    contents = "This is a test email sent from Python using yagmail."

    try:
        yag.send(to=receiver_email, subject=subject, contents=contents)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

send_email_yagmail()
