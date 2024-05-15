import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import os
import csv


my_email = 'test@gmail.com'
password_key = ''

#smtp server and port for gmail.com
gmail_server = "smtp.gmail.com"
gmail_port = 587

#starting connection
my_server = smtplib.SMTP(gmail_server,gmail_port)
my_server.ehlo()
my_server.starttls()

#login with your email and password
my_server.login(my_email, password_key)
#we use the ehlo method to identify the client to the server, its crucial to ensurethat your connection is secure 
#we enable encryption for the connection using Transport layer security bby calling the starttls() method
# we use the MIMEMultipart module to provide a class for creating MIME documents representing a multipart message
message = MIMEMultipart("alternative")

#adding text content  by using the MIMETet module that provides a class for creating MIME documents representing plain text in an email message

text_content= """
Hello {recruiter_name},I hope you are doing well. I'm Jane Doe, an engineering graduate with an Mtech in Computer Science and a specialization in Artificial Intelligence.

I am writing to inquire regarding open roles in {job_role} at {organization}. I have experience performing data analysis and modeling through my internships and research projects. I'm excited to have an opportunity to apply my skills and learn more in the organization.

I have attached my grade card and résumé below. Looking forward to hearing from you.

Thanks,
…… """

# message.attach(MIMEText(text_content))

#How to add images to my my email
#The MIMEImage module provides a class for creating MIME documents representing image data in an email
#we should import the MIMEImage and define the path that has your image file..
#Here we read its binary data and attach it to the messsage object as a MIMEImage

# #define your location
# my_image_path = 'C:\Users\HP 840 G3\OneDrive\me.jpg'

#Read teh imae from location 
# my_image = open(my_image_path,'rb').read()

# #ATTACH your image
# message.attach(MIMEImage(my_image, name = os.path.basename(my_image_path)))

#How to attach files to your email
#The MIMEApplication module here is used for creating MIME documents representing arbitirary binary data in an email message.It is often used for attaching files
#First u deine the document path, read its binary data and attach itto the message object as a MIMEApplication part.
#read the file from location 

# resume_file = ''

# with open (resume_file, 'rb') as f:
#     file = MIMEApplication(
#         f.read(),
#         name = os.path.basename(resume_file)
#     )
#     # Attach the file to the email message
#     file.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_file)}"')
#     message.attach(file)

with open("trials.csv") as csv_file:
    jobs = csv.reader(csv_file)
    next(jobs) #skipping the header row

    for row in jobs:
        # Check if all fields in the row are empty
        if all(not field.strip() for field in row):
            continue  # Skip empty row

        # Check if the row contains the expected number of fields
        if len(row) != 4:
            print(f"Ignoring row: {row} - Incorrect number of fields")
            continue  # Skip row with incorrect number of fields

        # Unpack row if it's not empty and contains the expected number of fields
        recruiter_name, recruiter_email, organization, job_role = row

        # Construct personalized email text
        email_text = text_content.format(recruiter_name=recruiter_name,
                                         organization=organization,
                                         job_role=job_role)

        # Attach the personalized text to the message
        message.attach(MIMEText(email_text))

        # Send the email
        my_server.sendmail(from_addr=my_email,
                           to_addrs=recruiter_email,
                           msg=message.as_string())


my_server.quit()