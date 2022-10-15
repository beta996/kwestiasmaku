import dataclasses

import requests
from bs4 import BeautifulSoup
import pandas as pd


@dataclasses.dataclass
class Recipe:
    url: str
    name: str
    ingredients: list[str]


page = 0
recipe_df = pd.DataFrame(columns=['link', 'name', 'ingredients'])
while True:

    html = requests.get(f'https://www.kwestiasmaku.com/przepisy/posilki?page={page}').text

    hrefs = []
    soup = BeautifulSoup(html, 'html.parser')
    soup = soup.find("div", {"class": "view-recipes-category"})
    recipes = soup.find_all("div", {"class": "col"})
    if len(recipes) == 0:
        print("Found all recipes!")
        break
    for recipe in recipes:
        href = recipe.find("a").get("href")
        hrefs.append(href)

    hrefs = [f'https://www.kwestiasmaku.com/{href}' for href in hrefs]

    for i, link in enumerate(hrefs):
        print(f"{i} link")
        html_recipe = requests.get(link).text
        soup = BeautifulSoup(html_recipe, 'html.parser')
        name = soup.find("h1", {"class": "przepis"}).get_text().strip()
        soup = soup.find("div", {"class": "group-skladniki"})
        if soup is None:
            print('no ingredients for recipe')
            continue
        ingredients = soup.find_all("li")
        ingredients = [ingredient.get_text().strip() for ingredient in ingredients]
        recipe = Recipe(link, name, ingredients)
        recipe_df = pd.concat(
            [recipe_df,
             pd.DataFrame(data={'link': recipe.url, 'name': recipe.name, 'ingredients': recipe.ingredients})])

    page += 1

recipe_df.to_csv('./all_recipes.csv', index=False)
