"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_profiles = {
        "High-Energy Pop": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "tempo_bpm": 125,
            "valence": 0.8,
            "danceability": 0.82,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
            "tempo_bpm": 78,
            "valence": 0.58,
            "danceability": 0.58,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "tempo_bpm": 148,
            "valence": 0.45,
            "danceability": 0.62,
            "likes_acoustic": False,
        },
    }

    for label, user_prefs in user_profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print(f"\n=== Profile: {label} ===")
        for rank, rec in enumerate(recommendations, start=1):
            song, score, explanation = rec
            print(f"{rank:>2}. {song['title']} by {song['artist']} | score={score:.2f}")
            print(f"    reasons: {explanation}")

    # Small sensitivity experiment: double energy weight and halve genre weight.
    experiment_profile = {
        **user_profiles["High-Energy Pop"],
        "weights": {
            "genre": 1.0,
            "mood": 1.2,
            "energy": 3.0,
            "tempo_bpm": 0.6,
            "valence": 0.5,
            "danceability": 0.4,
            "acousticness": 0.5,
        },
    }
    experiment_results = recommend_songs(experiment_profile, songs, k=3)
    print("\n=== Experiment: Energy x2, Genre x0.5 (High-Energy Pop) ===")
    for rank, rec in enumerate(experiment_results, start=1):
        song, score, explanation = rec
        print(f"{rank:>2}. {song['title']} by {song['artist']} | score={score:.2f}")
        print(f"    reasons: {explanation}")


if __name__ == "__main__":
    main()
