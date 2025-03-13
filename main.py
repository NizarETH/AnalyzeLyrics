import yt_dlp
import requests
from textblob import TextBlob


def get_video_title(youtube_url):
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict.get("title", "Titre inconnu")


def get_lyrics_from_ovh(song_title, artist_name):
    base_url = "https://api.lyrics.ovh/v1"
    url = f"{base_url}/{artist_name}/{song_title}"

    response = requests.get(url)
    data = response.json()

    if "lyrics" in data:
        return data["lyrics"]
    else:
        return "Paroles non trouvées"


def load_themes_keywords(file_path):
    themes_keywords = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                theme, keywords = line.strip().split(":")
                keywords_list = [keyword.strip() for keyword in keywords.split(",")]
                themes_keywords[theme.strip()] = keywords_list
    except FileNotFoundError:
        print(f"Le fichier {file_path} est introuvable.")
    except Exception as e:
        print(f"Une erreur est survenue: {e}")

    return themes_keywords


file_path = 'themes_keywords.txt'
themes_keywords = load_themes_keywords(file_path)

# Exemple d'utilisation
song_title = "Dernière tentative"
artist_name = "SPECY MEN"
lyrics = get_lyrics_from_ovh(song_title, artist_name)
#print(lyrics)
# Analyse de lyrics
blob = TextBlob(lyrics)
sentiment = blob.sentiment
themes_keywords = load_themes_keywords("./themes_keywords.txt")

theme_scores = {key: 0 for key in themes_keywords}

for theme, keywords in themes_keywords.items():
    for keyword in keywords:
        if keyword in lyrics.lower():
            theme_scores[theme] += 1

dominant_theme = max(theme_scores, key=theme_scores.get)
dominant_score = theme_scores[dominant_theme]


print("Analyse du contenu de la chanson :")
if dominant_score > 0:
    print(f"Le thème dominant semble être : {dominant_theme.capitalize()} (score : {dominant_score})")
else:
    print("Aucun thème dominant trouvé.")

if sentiment.polarity > 0:
    sentiment_result = "positif"
elif sentiment.polarity < 0:
    sentiment_result = "négatif"
else:
    sentiment_result = "neutre"


if sentiment.subjectivity > 0.5:
    subjectivity_result = "très subjectif (émotions personnelles)"
elif sentiment.subjectivity > 0:
    subjectivity_result = "quelque peu subjectif (opinion mais pas trop marquée)"
else:
    subjectivity_result = "objectif (faits, pas d'émotion)"


print(f"Sentiment général : {sentiment_result}")
print(f"Type de texte : {subjectivity_result}")