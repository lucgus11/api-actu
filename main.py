import feedparser
import json
import os
from datetime import datetime

SOURCES = {
    "RTBF Info": "https://rss.rtbf.be/article/rss/rtbfinfo_homepage.xml",
    "RTBF Monde": "https://rss.rtbf.be/article/rss/rtbfinfo_monde.xml",
    "7sur7": "https://www.7sur7.be/rss.xml",
    "7sur7 Monde": "https://www.7sur7.be/monde/rss.xml",
    "RTBF": "https://rss.rtbf.be/article/rss/rtbfinfo_homepage.xml",
    "7sur7": "https://www.7sur7.be/rss.xml",
    "Le Soir": "https://www.lesoir.be/rss/81851/extract.xml",
    "La Libre": "https://www.lalibre.be/rss/section/actu/belgique/",
    "RTL-info": "https://feeds.feedburner.com/rtlinfo/belgique",
    "Sud-info": "https://www.sudinfo.be/rss/2056/extract.xml",
    "France-info": "https://www.francetvinfo.fr/titres.rss",
    "RTBF-Belgique": "https://www.rtbf.be/info/rss/belgique.xml",
    "RTBF-Une": "https://www.rtbf.be/info/rss/actu.xml",
    "RTBF-Monde": "https://www.rtbf.be/info/rss/monde.xml",
    "RTBF-sport": "https://www.rtbf.be/sport/rss/sport.xml",
    "7sur7-Belgique": "https://www.7sur7.be/belgique/rss.xml",
    "7sur7-Monde": "https://www.7sur7.be/etranger/rss.xml",
    "7sur7-Sport": "https://www.7sur7.be/sport/rss.xml",
    "7sur7-people": "https://www.7sur7.be/show-biz/rss.xml",
    "Frandroid": "https://www.frandroid.com/feed",
    "Le Soir": "https://www.lesoir.be/rss/81851/tous_les_articles",
    "Le Soir-Belgique": "https://www.lesoir.be/rss/81862/belgique",
    "Le Soir-Monde": "https://www.lesoir.be/rss/81863/monde",
    "Le Soir-Sport": "https://www.lesoir.be/rss/81866/sports",
    "Le Soir-Culture": "https://www.lesoir.be/rss/81867/culture"
}

def fetch_news():
    # 1. Charger l'ancien fichier s'il existe pour ne pas perdre l'historique
    if os.path.exists('news.json'):
        with open('news.json', 'r', encoding='utf-8') as f:
            try:
                old_data = json.load(f)
                articles_archive = old_data.get("articles", [])
            except:
                articles_archive = []
    else:
        articles_archive = []

    # Créer un set des liens déjà enregistrés pour éviter les doublons
    known_links = {a['link'] for a in articles_archive}
    new_articles_count = 0

    # 2. Récupérer les nouvelles entrées
    for name, url in SOURCES.items():
        print(f"Vérification de : {name}...")
        feed = feedparser.parse(url)
        
        for entry in feed.entries: # On prend TOUT ce qui est dispo
            link = entry.get("link", "")
            
            # Si l'article n'est pas déjà dans notre archive
            if link not in known_links:
                new_article = {
                    "source": name,
                    "title": entry.get("title", "Sans titre"),
                    "link": link,
                    "published": entry.get("published", datetime.now().isoformat()),
                    "summary": entry.get("summary", "").split('<')[0][:200] # Limite à 200 car.
                }
                articles_archive.append(new_article)
                known_links.add(link)
                new_articles_count += 1

    # 3. Trier par date et limiter à l'historique récent (ex: les 100 derniers articles)
    # Note: On garde un historique pour que l'API soit riche
    articles_archive.sort(key=lambda x: x.get('published', ''), reverse=True)
    final_list = articles_archive[:100] 

    # 4. Sauvegarder
    output = {
        "last_update": datetime.now().isoformat(),
        "new_articles_added": new_articles_count,
        "total_articles": len(final_list),
        "articles": final_list
    }

    with open('news.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    
    print(f"Terminé ! {new_articles_count} nouveaux articles ajoutés.")

if __name__ == "__main__":
    fetch_news()
