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
    eng_ingredients = translate(ingredients)
    pl_list_ingredients = ingredients.split(' ')
    list_ingredients = eng_ingredients.split(' ')
    recipes_df = pd.read_csv('./translated_all_recipes.csv')
    recipes_df = recipes_df.dropna()
    link_list = []
    link_dict = {}
    for ing in list_ingredients:
        link_dict.setdefault(ing, [])

    for index, row in recipes_df.loc[:,['link','eng_ingredients']].iterrows():
        for input_ingr in list_ingredients:
            if input_ingr.lower() in row['eng_ingredients'].lower():
                link_dict[input_ingr].append(row['link'])
            link_list = []
    sets = [set(one_set) for one_set in list(link_dict.values())]
    result = set(list(link_dict.values())[0])
    for s in sets:
        result = result.intersection(s)
    print(result)

    return render_template('display_recipes.html', list_ingredients=list(zip(pl_list_ingredients, list_ingredients)), links=result)
