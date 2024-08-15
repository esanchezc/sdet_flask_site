from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from flask import Flask, jsonify, render_template, g, request
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = os.getenv("EMAIL_USERNAME")
SMTP_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", SMTP_USERNAME)


def load_cv():
    if "cv" not in g:
        with open("cv.json", "r") as file:
            g.cv = json.load(file)
    return g.cv


@app.before_request
def before_request():
    g.cv = load_cv()


def send_email(subject, body,from_email, to_email):
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


@app.route("/", methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]

        email_subject = f"New contact from {name}: {subject}"
        email_body = (
            f"Name: {name}\nEmail: {email}\nSubject: {subject}\nMessage: {message}"
        )

        if send_email(email_subject, email_body, SMTP_USERNAME, RECIPIENT_EMAIL):
            return jsonify(
                {"status": "success", "message": "Message sent successfully!"}
            )
        else:
            return jsonify(
                {
                    "status": "error",
                    "message": "Failed to send message. Please try again later.",
                }
            )

    return render_template("home.html", cv=g.cv)


@app.route("/experience/<int:company_index>")
def get_experience(company_index):
    try:
        experience = g.cv["work_experience"][company_index]
        return render_template("experience.html", experience=experience)
    except IndexError:
        return "Experience not found", 404


# @app.route("/contact", methods=["POST"])
# def send_contact_request():
#     name = request.form['name']
#     email = request.form['email']
#     subject = request.form['subject']
#     message = request.form['message']
#     return jsonify({"status": "success", "message": "Message sent successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
