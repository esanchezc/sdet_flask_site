import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/emanuel")
def cv():
    with open("cv.json", 'r') as file:
        file_contents = file.read()
        cv = json.loads(file_contents)    
    return render_template('emanuel.html', summary=cv['summary'])

if __name__ == "__main__":
    app.run(debug=True)