from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

mood_to_genre = {
    "happy": ["pop", "dance", "electronic", "reggaeton", "tropical house"],
    "sad": ["blues", "jazz", "classical", "sufi", "qawwali", "ambient"],
    "relaxed": ["chill", "acoustic", "lo-fi", "easy listening", "jazz"],
    "energetic": ["rock", "punk", "metal", "hip-hop", "trap", "dubstep"],
    "romantic": ["love songs", "romantic pop", "acoustic", "soft rock"],
    "party": ["dance", "house", "edm", "trap", "hip-hop", "reggaeton"],
    "chill": ["chill-out", "ambient", "lo-fi", "indie"],
    "spiritual": ["sufi", "qawwali", "devotional", "new age", "classical"],
    "nostalgic": ["oldies", "classic rock", "retro", "disco", "80s pop"],
    "motivational": ["rock", "hip-hop", "pop", "electronic", "indie"],
    "bollywood": ["bollywood", "filmi", "indian pop"],
    "rap": ["hip hop", "rap", "hindi hip hop", "desi hip hop", "drill", "trap"]
}


def analyze_mood(mood: str, top_k: int = 2):
    candidate_moods = list(mood_to_genre.keys())
    
    mood_predictions = classifier(
        mood,
        candidate_labels=candidate_moods,
        multi_label=True,
        hypothesis_template="This is suitable for a {} playlist."
    )

    labels = mood_predictions['labels']
    scores = mood_predictions['scores']

    print("\nMood Scores:")
    for label, score in zip(labels, scores):
        print(f"{label}: {score:.4f}")

    top_labels = [labels[i] for i in range(top_k)]
    
    genres = []
    for label in top_labels:
        genres.extend(mood_to_genre.get(label, []))

    return list(set(genres))