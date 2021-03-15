from email.mime.text import MIMEText
import smtplib
def send_email(email,height,average_height,count):
    from_email="testprojecttt2021@gmail.com"
    from_password="qM19931125"
    to_email=email

    subject="Height data"
    message="Hey there, your height is  <strong>{}</strong>. Average height  is calculated of <strong>{}</strong> people is <strong>{} cm</strong>. " .format(height,count,average_height)

    msg=MIMEText(message,'html')
    msg['Subject']=subject
    msg['To']=to_email
    msg['From']=from_email

    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email,from_password)
    gmail.send_message(msg)