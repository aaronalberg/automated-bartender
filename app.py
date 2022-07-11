from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
app = Flask(__name__)


@app.route("/")
def home():
   templateData = {
      'drinks': ["oj", "gin", "rum"]
      }
   return render_template('index.html', **templateData)

@app.route("/make/", methods=['POST'])
def move_forward():
    drink = request.form['drink']
    print("request received to make " + drink)
    return render_template('makingdrink.html', drink=drink);


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)