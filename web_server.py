import pandas as pd
from flask import Flask, render_template, request
from translation import translate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/display_recipes")
def display():
    ingredients = request.args.get('list_ingredients', '')
    ingredients = translate(ingredients)
    list_ingredients = ingredients.split(' ')
    recipes_df = pd.read_csv('./translated_all_recipes.csv')
    recipes_df = recipes_df.dropna()
    link_list = []
    for index, row in recipes_df.loc[:,['link','eng_ingredients']].iterrows():
        for input_ingr in list_ingredients:
            if input_ingr.lower() in row['eng_ingredients'].lower():
                print(link_list.append(row['link']))

    return render_template('display_recipes.html', list_ingredients=list_ingredients, links=link_list)