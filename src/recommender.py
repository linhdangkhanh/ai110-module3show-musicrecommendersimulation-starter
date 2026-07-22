import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            score, reasons = score_song(user_prefs, song_dict)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries with typed values."""
    songs = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences; returns (score, list_of_reasons)."""
    reasons = []

    # Genre match (0.30 weight)
    genre_score = 1.0 if song["genre"] == user_prefs.get("genre", "") else 0.0
    if genre_score == 1.0:
        reasons.append(f"Matches your love of {song['genre']}")

    # Mood match (0.25 weight)
    mood_score = 1.0 if song["mood"] == user_prefs.get("mood", "") else 0.0
    if mood_score == 1.0:
        reasons.append(f"Has the {song['mood']} vibe you enjoy")

    # Energy proximity (0.25 weight)
    target_energy = user_prefs.get("energy", 0.5)
    energy_diff = abs(target_energy - song["energy"])
    energy_score = 1.0 - energy_diff
    if energy_diff <= 0.15:
        reasons.append(f"Energy level ({song['energy']:.2f}) fits your preference")

    # Acoustic match (0.20 weight)
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acoustic_score = song["acousticness"]
    else:
        acoustic_score = 1.0 - song["acousticness"]
    if (likes_acoustic and song["acousticness"] >= 0.6) or (not likes_acoustic and song["acousticness"] <= 0.4):
        label = "acoustic" if likes_acoustic else "electronic"
        reasons.append(f"Is {label} like you prefer")

    # Weighted sum
    total = (
        0.30 * genre_score
        + 0.25 * mood_score
        + 0.25 * energy_score
        + 0.20 * acoustic_score
    )

    return total, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score all songs, rank descending, and return top-k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
