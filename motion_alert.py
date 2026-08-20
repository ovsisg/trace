import smtplib
from PIL import Image
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Motion detected"
    email_message.set_content("Motion was detected by your camera.")

    host = "smtp.gmail.com"
    port = 587

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    # Read the image file as binary data 
    with open(image_path, "rb") as file:
        content = file.read()

    # Get the format of the image
    with Image.open(image_path) as image:
        image_format = image.format.lower()

    # Attach the image to the email
    email_message.add_attachment(content, maintype="image", subtype=image_format)

    gmail = smtplib.SMTP(host, port)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(sender, password)
    gmail.sendmail(sender, receiver, email_message.as_string())
    gmail.quit()