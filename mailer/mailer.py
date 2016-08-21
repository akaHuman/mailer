import argparse
import re
import os
import ntpath
import smtplib
import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")


def is_valid_email(email):
    return EMAIL_REGEX.match(email)


def is_file(path):
    if os.path.isfile(path):
        return path
    raise argparse.ArgumentTypeError("Attachment can only be a file but " + path + " is not.")


sender_email = raw_input("Gmail Address: ")
if not is_valid_email(sender_email):
    print sender_email + " is not a valid email address"
    exit(1)

password = getpass.getpass()

arg_parser = argparse.ArgumentParser(description='Send email to multiple addresses.')
arg_parser.add_argument('receivers', type=file)
arg_parser.add_argument('subject', type=str)
arg_parser.add_argument('-b', '--body', required=False, type=file)
arg_parser.add_argument('-a', '--attachments', required=False, type=is_file, nargs='*')

args = arg_parser.parse_args()

msg = MIMEMultipart()
msg['From'] = sender_email
msg['Subject'] = args.subject

body = args.body.read()
msg.attach(MIMEText(body, 'plain'))

print msg.as_string()
print "Attachments: "
if args.attachments is not None:
    for path in args.attachments:
        print path
        filename = ntpath.basename(path)
        with open(path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)

to_list = args.receivers.read().splitlines()
print "Receiver addresses: " + str(to_list)

response = raw_input("Continue? [y/n]: ")
if response == 'y' or response == 'Y':
    server = None
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

    except smtplib.SMTPConnectError as err:
        print "Unable to connect to SMTP server."
        server.quit()
        exit(2)
    except smtplib.SMTPAuthenticationError as err:
        print "Login attempt failed. Incorrect username/password or " \
                "the account does not allow less secure apps to login."
        server.quit()
        exit(3)

    if server is not None:
        try:
            for address in to_list:
                address = str(address).strip()
                if is_valid_email(address):
                    msg.__delitem__('To')
                    msg['To'] = address
                    text = msg.as_string()
                    print "Sending mail to: " + address
                    try:
                        server.sendmail(sender_email, address, text)
                    except Exception:
                        print "Exception while sending mail."
                else:
                    print address + " is not a valid email. Skipping."
        finally:
            server.quit()
