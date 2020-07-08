import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
from decouple import config

sender_email = config('SENDER_EMAIL')
password = config("SENDER_PASSWORD")


def sendmail(receiver, message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver, message.as_string())


def message_generator(mail_data):
    message = MIMEMultipart("alternative")
    message["Subject"] = mail_data["subject"]
    message["From"] = sender_email
    message["To"] = mail_data["receiver_email"]
    text = mail_data["text"]
    html = mail_data["html"]
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    return message


def personify(user_list, context):

    frontend_url = "http://localhost:3000/"
    subject = ""
    text = ""
    html = ""

    if context["action"] == "new_team_member":
        subject = "Welcome Aboard!"
        text = f"""You have been added to the project {context['project'].name}"""
        html = f"""\
            <html>
                <body style='text-align:center;'>
                    <h1 style='color:purple;'>Chronicles</h1><hr />
                    <p>Congratulations on making into Project <strong>{context['project'].name}</strong>!</p><hr />
                </body>
            </html>
        """

    elif context["action"] == "bug_report_update":
        subject = f"New Bug found in {context['project'].name} 😟"
        text = f"""There is a new bug report in {context['project'].name}. 
            Visit {frontend_url+context['project'].slug}/
        """
        html = f"""\
            <html>
                <body style='text-align:center;'>
                    <h1 style='color:purple;'>Chronicles</h1><hr />
                    <p>Project <strong>{context['project'].name}</strong> has a new bug report 
                    entitled {context['bug_report'].heading}.</p>
                    <p>Visit Chronicles and fix it ASAP!</p>
                    <a href="{frontend_url+context['project'].slug}/">Link to the Project</a><hr />
                </body>
            </html>
        """

    elif context["action"] == "bug_report_assignment":
        subject = f"Bug report assigned to you!"
        text = f"""A bug of project {context['project'].name} has been assigned to you.
            Visit {frontend_url} to find out more.
        """
        html = f"""\
            <html>
                <body style='text-align:center;'>
                    <h1 style='color:purple;'>Chronicles</h1><hr />
                    <p>A bug in the project <strong>{context['project'].name}</strong> has been assigned to you.</p>
                    <p>Heading: {context['bug_report'].heading}</p>
                    <p>Visit Chronicles and fix it ASAP!</p>
                    <a style="color:'purple'; text-decoration: 'none'" href="{frontend_url}/">Chronicles</a><hr />
                </body>
            </html>
        """

    elif context["action"] == "bug_resolved":
        subject = f"Bug report resolved 😊"
        text = f"""A bug of project {context['project'].name} has been resolved!"""
        html = f"""\
            <html>
                <body style='text-align:center;'>
                    <h1 style='color:purple;'>Chronicles</h1><hr />
                    <h3>Wohoo!</h3>
                    <p>A bug report from project <strong>{context['project'].name}</strong> was resolved!</p>
                    <h4>Heading of bug report:</h4>
                    <p>{context['bug_report'].heading}</p><hr />
                </body>
            </html>
        """

    if (subject != "") and (text != "") and (html != ""):
        for user in user_list:
            mail_data = {
                "receiver_email": user.email,
                "subject": subject,
                "text": text,
                "html": html,
            }

            message = message_generator(mail_data)
            print("Sending email")
            sendmail(user.email, message)
            print("Mail sent")
    else:
        print("No data")


class MailThread(threading.Thread):
    def __init__(self, user_list, context, *args, **kwargs):
        self.user_list = user_list
        self.context = context
        super(MailThread, self).__init__(*args, **kwargs)

    def run(self):
        personify(self.user_list, self.context)
        return
