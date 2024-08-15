from flask import Flask, render_template, g, request
import json

app = Flask(__name__)

def load_cv():
    if 'cv' not in g:
        with open("cv.json", 'r') as file:
            g.cv = json.load(file)
    return g.cv

@app.before_request
def before_request():
    g.cv = load_cv()

@app.route("/")
def main_page():
    return render_template('home.html', cv=g.cv, msg_sent=False)

@app.route("/experience/<int:company_index>")
def get_experience(company_index):
    try:
        experience = g.cv['work_experience'][company_index]
        return render_template('experience.html', experience=experience)
    except IndexError:
        return "Experience not found", 404
    
@app.route("/contact", methods=["POST"])
def send_contact_request():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']
    return render_template('home.html', cv=g.cv, msg_sent=True)

if __name__ == "__main__":
    app.run(debug=True)