import os

import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-pl-en"
headers = {"Authorization": f"Bearer {os.getenv('HUGGINGFACE_ACCESS_TOKEN')}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json(), response.status_code


def translate(text:str):
    output, status_code = query({"inputs": text.lower()})
    if status_code != 200:
        raise RuntimeError(f"Status not 200! But {status_code}")
    return output[0]['translation_text']


if __name__ == '__main__':

    recipe_df = pd.read_csv('./translated_all_recipes.csv')

    for i, ingr in enumerate(recipe_df['ingredients']):
        if not pd.isnull(recipe_df.loc[i, 'eng_ingredients']):
            continue
        output, status_code = query({
            "inputs": ingr,
        })
        if status_code != 200:
            print(output)
            break
        print(f"{i} out of {len(recipe_df)} | {output}")
        recipe_df.loc[i, 'eng_ingredients'] = output[0]['translation_text']
        recipe_df.to_csv('./translated_all_recipes.csv', index=False)
