import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDERMAIL="notificationbot34@gmail.com"
SENDERPASS="nnys rpvz hjjw lyit"


def startserver():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDERMAIL, SENDERPASS)
    
    return server

def exitserver(server):
    server.quit()


def sendmail(receiver,body):
    message=MIMEMultipart()
    message["From"]=SENDERMAIL
    message["To"]=receiver
    message["Subject"]="Notification"
    message.attach(MIMEText(body,"plain"))
    
    try:
        server=startserver()
        server.sendmail(SENDERMAIL,receiver,message.as_string())
        exitserver(server)

    except Exception as e:
        print(f"Error sending mail: {str(e)}")
        return e
    

    print(f"Mail sent to {receiver}")

sinchpass="vGBkjp#6W$BhUMs"

KEYSECRET="8fG~DKetmq--y_OuFkc2oCqVyM"