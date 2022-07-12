from flask import Flask, render_template, request, url_for, flash, redirect
import datetime
import json

app = Flask(__name__)

file = open("drinks.json")
drinks = json.load(file)["drinks"]
MAX_PUMPS = 6

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

@app.route("/make", methods=['POST'])
def make_drink():
    drink = request.form['drink']
    print("request received to make " + drink)

    templateData = {
      'drink': find_drink(drink, drinks)
      }
    return render_template('makingdrink.html', **templateData);

@app.route("/add-drink", methods=['POST'])
def add_drink():
   new_drink = {}
   new_drink['name'] = request.form['new-drink-name']

   ingredients = []
   for i in range(1, MAX_PUMPS + 1):
      label = 'new-drink-ingredient-' + str(i)
      if label not in request.form:
         break

      request.form['new-drink-ingredient-' + str(i)]
      new_ingredient = {
         "name": request.form['new-drink-ingredient-' + str(i)],
         "quantity": request.form['new-drink-quantity-' + str(i)]
      }
      
      ingredients.append(new_ingredient)
   
   new_drink['ingredients'] = ingredients
   drinks.append(new_drink)
   data = { "drinks": drinks }

   with open('drinks.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

   templateData = {
      'drinks': drinks
      }
   return render_template('index.html', **templateData)

@app.route("/create-page", methods=['GET', 'POST'])
def create_page():
   templateData = {
      'number_ingredients': int(request.form['number-ingredients'])
      }

   return render_template('createpage.html', **templateData)







if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)