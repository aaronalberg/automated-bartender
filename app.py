from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
import json

app = Flask(__name__)

file = open("drinks.json")
drinks = json.load(file)["drinks"]

def find_drink(drink, drinks):
   for i in drinks:
      if i["name"] == drink:
         return i
      print(i)         
   return "NOT FOUND"


@app.route("/")
def home():
   templateData = {
      'drinks': drinks
      }
   return render_template('index.html', **templateData)

@app.route("/make/", methods=['POST'])
def make_drink():
    drink = request.form['drink']
    print("request received to make " + drink)

    templateData = {
      'drink': find_drink(drink, drinks)
      }
    return render_template('makingdrink.html', **templateData);


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)