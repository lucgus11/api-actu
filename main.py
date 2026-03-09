import feedparser
import json
import os
from datetime import datetime

# Configuration des sources
SOURCES = {
    "RTBF": "https://rss.rtbf.be/article/rss/rtbfinfo_homepage.xml",
    "7sur7": "https://www.7sur7.be/rss.xml",
    "Le Soir": "https://www.lesoir.be/rss/81851/extract.xml"
}

def clean_date(date_str):
    """Convertit les dates RSS en format ISO lisible."""
    try:
        # On tente de parser la date standard des flux RSS
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
        return dt.isoformat()
    except:
        return date_str

def fetch_news():
    full_data = {
        "last_update": datetime.now().isoformat(),
        "article_count": 0,
        "articles": []
    }

    for name, url in SOURCES.items():
        print(f"Récupération de : {name}...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries[:15]:  # On prend les 15 derniers par source
            article = {
                "source": name,
                "title": entry.get("title", "Sans titre"),
                "link": entry.get("link", ""),
                "description": entry.get("summary", "").split('<')[0], # Nettoyage HTML basique
                "published": clean_date(entry.get("published", "")),
                "category": entry.get("category", "Général")
            }
            full_data["articles"].append(article)

    # Tri par date (du plus récent au plus ancien)
    full_data["articles"].sort(key=lambda x: x['published'], reverse=True)
    full_data["article_count"] = len(full_data["articles"])

    # Sauvegarde
    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)
    print("Fichier news.json généré avec succès.")

if __name__ == "__main__":
    fetch_news()
