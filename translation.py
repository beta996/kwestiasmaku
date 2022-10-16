import os

import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-pl-en"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_ACCESS_TOKEN')}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


recipe_df = pd.read_csv('./translated_all_recipes.csv')

for i, ingr in enumerate(recipe_df['ingredients']):
    if not pd.isnull(recipe_df.loc[i, 'eng_ingredients']):
        continue
    output = query({
        "inputs": ingr,
    })
    print(f"{i} out of {len(recipe_df)} | {output}")
    recipe_df.loc[i, 'eng_ingredients'] = output[0]['translation_text']
    recipe_df.to_csv('./translated_all_recipes.csv', index=False)