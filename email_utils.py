import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from speech_utils import speak, listen
def send_email_with_attachments(subject, body, sender_email, password, receiver_email, attachments):
    # Create the email
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Add body
    msg.attach(MIMEText(body, 'plain'))

    # Attach files
    for file_path in attachments:
        with open(file_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {file_path.split("/")[-1]}',
            )
            msg.attach(part)

    # Send the email
    try:
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
        speak("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
        speak(f"Error sending email: {e}")