"""Reliability harness for the final applied AI recommender project."""

from __future__ import annotations

from statistics import mean
from typing import Dict, List

try:
    from .recommender import confidence_from_score, load_songs, recommend_songs
except ImportError:
    from recommender import confidence_from_score, load_songs, recommend_songs


def run_reliability_checks() -> List[Dict]:
    songs = load_songs("data/songs.csv")

    checks = [
        {
            "name": "High-Energy Pop",
            "user": {
                "genre": "pop",
                "mood": "happy",
                "energy": 0.85,
                "tempo_bpm": 125,
                "valence": 0.8,
                "danceability": 0.82,
                "likes_acoustic": False,
            },
            "expect": lambda recs: recs[0][0]["genre"] == "pop",
            "expectation": "Top-1 genre should be pop",
        },
        {
            "name": "Chill Lofi",
            "user": {
                "genre": "lofi",
                "mood": "chill",
                "energy": 0.35,
                "tempo_bpm": 78,
                "valence": 0.58,
                "danceability": 0.58,
                "likes_acoustic": True,
            },
            "expect": lambda recs: recs[0][0]["genre"] == "lofi",
            "expectation": "Top-1 genre should be lofi",
        },
        {
            "name": "Deep Intense Rock",
            "user": {
                "genre": "rock",
                "mood": "intense",
                "energy": 0.92,
                "tempo_bpm": 148,
                "valence": 0.45,
                "danceability": 0.62,
                "likes_acoustic": False,
            },
            "expect": lambda recs: recs[0][0]["genre"] == "rock",
            "expectation": "Top-1 genre should be rock",
        },
        {
            "name": "Guardrail Out-of-Range Input",
            "user": {
                "genre": "pop",
                "mood": "happy",
                "energy": 1.7,
                "tempo_bpm": -25,
                "valence": 1.4,
                "danceability": -0.2,
                "likes_acoustic": False,
            },
            "expect": lambda recs: len(recs) == 3 and 0.0 <= recs[0][1],
            "expectation": "System should return valid scores after clamping",
        },
    ]

    results: List[Dict] = []
    for check in checks:
        recs = recommend_songs(check["user"], songs, k=3)
        passed = bool(check["expect"](recs))
        top_song, top_score, _ = recs[0]
        conf = confidence_from_score(top_score, check["user"])
        results.append(
            {
                "name": check["name"],
                "expectation": check["expectation"],
                "passed": passed,
                "top_song": f"{top_song['title']} ({top_song['genre']})",
                "top_score": round(top_score, 3),
                "confidence": conf,
            }
        )

    return results


def main() -> None:
    results = run_reliability_checks()
    passed = sum(1 for r in results if r["passed"])
    confidences = [r["confidence"] for r in results]

    print("=== Reliability Harness ===")
    for idx, row in enumerate(results, start=1):
        status = "PASS" if row["passed"] else "FAIL"
        print(
            f"{idx}. [{status}] {row['name']} | expected: {row['expectation']} | "
            f"top={row['top_song']} score={row['top_score']:.3f} conf={row['confidence']:.3f}"
        )

    print("\n=== Summary ===")
    print(f"Passed {passed}/{len(results)} checks")
    print(f"Average confidence: {mean(confidences):.3f}")


if __name__ == "__main__":
    main()
