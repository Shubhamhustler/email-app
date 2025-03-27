import os
import smtplib
import ssl
from flask import Flask, request, render_template, redirect, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "shubhamsngh550@gmail.com"
SENDER_PASSWORD = "your-app-password"  # Use an App Password, NOT your real password!

PDF_PATH = "Shubham_Singh_CV.pdf"  # Ensure this file is in the same directory
RECIPIENTS_FILE = "recipients.txt"  # Editable online

# Function to read recipients from a file
def get_recipients():
    recipients = []
    if os.path.exists(RECIPIENTS_FILE):
        with open(RECIPIENTS_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",", 1)
                email = parts[0].strip()
                name = parts[1].strip() if len(parts) > 1 else "The Hiring Team"
                recipients.append((email, name))
    return recipients

# Email Template
email_template = """\
<html>
  <body>
    <p>Dear {name},</p>
    <p>I hope you are doing well. I came across the <b> Software Engineer</b> job opening and am eager to apply.</p>
    <p>With <b> Around 3 </b> years of experience in <b> software development </b>, specializing in <b>Angular, Java, Spring Boot, Microservices, Docker, Linux, MySQL, MongoDB, SNMP, REST API, APM (DataDog, NewRelic)</b>. </p>
    <p>Please find my resume attached. Looking forward to your response.</p>
    <p>Best regards,<br>Shubham Singh<br>7668701292</p>
  </body>
</html>
"""

# Function to send email
def send_email(email, name):
    try:
        msg = MIMEMultipart()
        msg["From"] = "Shubham Singh"
        msg["To"] = email
        msg["Subject"] = "Application for Software Engineer"

        # Personalized email
        msg.attach(MIMEText(email_template.format(name=name), "html"))

        # Attach CV
        with open(PDF_PATH, "rb") as pdf_file:
            pdf_part = MIMEApplication(pdf_file.read(), _subtype="pdf")
            pdf_part.add_header("Content-Disposition", "attachment", filename=PDF_PATH)
            msg.attach(pdf_part)

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls(context=context)
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())

        print(f"Email sent to {name} ({email})")
        return True
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")
        return False

# Route to display form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Send emails to all recipients
        recipients = get_recipients()
        for email, name in recipients:
            send_email(email, name)
        return "Emails sent successfully!"

    return render_template("index.html", recipients=get_recipients())

# Route to update recipients list
@app.route("/update_recipients", methods=["POST"])
def update_recipients():
    new_content = request.form["recipients"]
    with open(RECIPIENTS_FILE, "w") as file:
        file.write(new_content)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

