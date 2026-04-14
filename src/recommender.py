from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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
        """Return top-k Song objects sorted by descending compatibility score."""
        scored: List[Tuple[Song, float]] = []
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        for song in self.songs:
            score, _ = score_song(user_prefs, song.__dict__)
            scored.append((song, score))

        scored.sort(key=lambda item: item[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain score components for a specific Song and UserProfile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        _, reasons = score_song(user_prefs, song.__dict__)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs: List[Dict] = []
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    with open(csv_path, mode="r", encoding="utf-8", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            parsed: Dict = {}
            for key, value in row.items():
                if key in int_fields:
                    parsed[key] = int(value)
                elif key in float_fields:
                    parsed[key] = float(value)
                else:
                    parsed[key] = value
            songs.append(parsed)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons: List[str] = []
    weights = user_prefs.get("weights", {})

    genre_weight = float(weights.get("genre", 2.0))
    mood_weight = float(weights.get("mood", 1.2))
    energy_weight = float(weights.get("energy", 1.5))
    tempo_weight = float(weights.get("tempo_bpm", 0.6))
    valence_weight = float(weights.get("valence", 0.5))
    danceability_weight = float(weights.get("danceability", 0.4))
    acoustic_weight = float(weights.get("acousticness", 0.5))

    # Weighted categorical matches
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    # Numeric closeness: higher points when near user target
    target_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_points = max(0.0, energy_weight * (1.0 - abs(song_energy - target_energy)))
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    target_tempo = float(user_prefs.get("tempo_bpm", 110.0))
    song_tempo = float(song.get("tempo_bpm", 110.0))
    # Tempo scale is wider, so normalize by a broad window.
    tempo_points = max(0.0, tempo_weight * (1.0 - min(abs(song_tempo - target_tempo) / 100.0, 1.0)))
    score += tempo_points
    reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    target_valence = float(user_prefs.get("valence", 0.6))
    song_valence = float(song.get("valence", 0.6))
    valence_points = max(0.0, valence_weight * (1.0 - abs(song_valence - target_valence)))
    score += valence_points
    reasons.append(f"valence closeness (+{valence_points:.2f})")

    target_danceability = float(user_prefs.get("danceability", 0.65))
    song_danceability = float(song.get("danceability", 0.65))
    danceability_points = max(0.0, danceability_weight * (1.0 - abs(song_danceability - target_danceability)))
    score += danceability_points
    reasons.append(f"danceability closeness (+{danceability_points:.2f})")

    likes_acoustic = bool(user_prefs.get("likes_acoustic", False))
    acousticness = float(song.get("acousticness", 0.0))
    if likes_acoustic:
        acoustic_points = acoustic_weight * acousticness
        score += acoustic_points
        reasons.append(f"acoustic preference (+{acoustic_points:.2f})")
    else:
        non_acoustic_points = acoustic_weight * (1.0 - acousticness)
        score += non_acoustic_points
        reasons.append(f"non-acoustic preference (+{non_acoustic_points:.2f})")

    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored_songs: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    ranked = sorted(scored_songs, key=lambda item: item[1], reverse=True)

    top_k: List[Tuple[Dict, float, str]] = []
    for song, score, reasons in ranked[:k]:
        top_k.append((song, score, "; ".join(reasons)))

    return top_k
