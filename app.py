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
   new_name = request.form['new-drink-name'].lower()
   if find_drink(new_name, drinks) != "NOT FOUND":
      return redirect("/")
   new_drink = {}
   new_drink['name'] = new_name

   ingredients = []
   for i in range(1, MAX_PUMPS + 1):
      # have processed all ingredients provided
      if request.form['new-drink-ingredient-' + str(i)].lower() not in request.form:
         break

      new_ingredient_name = request.form['new-drink-ingredient-' + str(i)].lower()
      new_ingredient_quantity = request.form['new-drink-quantity-' + str(i)]
      try:
         new_ingredient_name = request.form['new-drink-ingredient-' + str(i)].lower()
         new_ingredient_quantity = int(request.form['new-drink-quantity-' + str(i)])
         if new_ingredient_quantity <= 0:
            raise ValueError("negative")
      except ValueError:
         print("ERRORORED")
         return redirect("/")

      new_ingredient = {
         "name": new_ingredient_name,
         "quantity": new_ingredient_quantity
      }
      
      ingredients.append(new_ingredient)
   
   new_drink['ingredients'] = ingredients
   drinks.append(new_drink)
   data = { "drinks": drinks }

   with open('drinks.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

   return redirect('/')

@app.route("/create-page", methods=['GET', 'POST'])
def create_page():
   templateData = {
      'number_ingredients': int(request.form['number-ingredients'])
      }

   return render_template('createpage.html', **templateData)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)