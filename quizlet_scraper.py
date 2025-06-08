import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def extract_flashcards(quizlet_url):
    res = requests.get(quizlet_url)
    soup = BeautifulSoup(res.text, 'html.parser')
    data = []
    # Quizlet uses embedded JSON for flashcards, so we look for it
    for script in soup.find_all('script'):
        if 'window.Quizlet' in script.text:
            json_text = script.text
            break
    else:
        print(f"Could not find flashcards in {quizlet_url}")
        return []
    # Extract terms and definitions using regex
    matches = re.findall(r'"term":"(.*?)","definition":"(.*?)"', json_text)
    for q, a in matches:
        data.append({'question': q, 'answer': a, 'source_url': quizlet_url})
    return data

# Paste your links here, grouped by class
quizlet_links = {
    "AP Psychology": [
        "https://quizlet.com/205747060/ap-psychology-all-units-flash-cards/",
        "https://quizlet.com/888920633/ap-psychology-all-units-flash-cards/",
        "https://quizlet.com/203971598/ap-psychology-all-units-flash-cards/"
    ],
    # ... (add all your other classes and links here)
}

for class_name, links in quizlet_links.items():
    all_cards = []
    for url in links:
        print(f"Extracting from {url}")
        all_cards.extend(extract_flashcards(url))
    if all_cards:
        df = pd.DataFrame(all_cards)
        df.to_csv(f"{class_name.replace(' ', '_')}_flashcards.csv", index=False)
        print(f"Saved {len(all_cards)} cards for {class_name}")
    else:
        print(f"No cards found for {class_name}")
