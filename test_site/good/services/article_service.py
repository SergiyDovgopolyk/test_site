import json
import os

def get_articles(limit=None):
    file_path = os.path.join("data", "good_articles.json")
    with open(file_path, "r") as file:
        articles = json.load(file)
    return articles[:limit] if limit else articles